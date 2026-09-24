import re
import logging
from typing import Tuple
from openai import OpenAI

logger = logging.getLogger("Guardrails")

class RegexGuardrail:
    """Fast, deterministic check for system leaks, API keys, and sensitive actions."""

    SAFE_GUARDRAIL_POLICY = {
        "input_policy": [
            "Block prompt-injection attempts in raw untrusted input before any model call.",
            "Reject requests that attempt to override instructions, reveal hidden prompts, or instruct the model to ignore prior rules.",
            "Treat user content as untrusted data and never execute instructions embedded in that payload.",
        ],
        "output_policy": [
            "Regex-check generated text for prompt leaks, secret leaks, financial abuse, and command execution.",
            "Run a second semantic classification pass on model output before sending it to the user.",
            "Deny any output that contains policy violations or risky action requests.",
        ],
    }

    PATTERNS = {
        "api_key_leak": r"(sk-[A-Za-z0-9]{20,}|AIzaSy[a-zA-Z0-9_-]{33}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})",
        "system_prompt_leak": r"(?:ignore\s+(?:all\s+)?previous\s+instructions|system\s+(?:override|prompt)|developer\s+prompt|reveal\s+(?:your\s+)?(?:system|developer)\s+prompt|override\s+.*instructions|\[system\s+override\])",
        "unauthorized_financial": r"(\$?\d{1,3}(,\d{3})*(\.\d{2})?)\s*(transfer|wire|payment|account)",
        "command_injection": r"(rm\s+-rf|sudo\s+|chmod\s+777|curl\s+http|powershell\s+-enc)",
    }

    @classmethod
    def validate(cls, text: str) -> Tuple[bool, str]:
        if text is None:
            return False, "Rule Violation: empty_input"

        for rule_name, pattern in cls.PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"Regex Guardrail Triggered: '{rule_name}'")
                return False, f"Rule Violation: {rule_name}"
        return True, "Passed"

    @classmethod
    def validate_input(cls, text: str) -> Tuple[bool, str]:
        """Block prompt injections before they reach a model call."""
        if not isinstance(text, str):
            return False, "Rule Violation: invalid_input_type"

        trimmed = text.strip()
        if not trimmed:
            return False, "Rule Violation: empty_input"

        return cls.validate(trimmed)


class SemanticGuardrail:
    """Context-aware output evaluator using local Llama 3.2."""
    
    def __init__(self, client: OpenAI, model_name: str = "llama3.2"):
        self.client = client
        self.model_name = model_name

    def validate_output(self, user_prompt: str, candidate_response: str) -> Tuple[bool, str]:
        logger.info(f"[Step 3b] Running Local Semantic Guardrail ({self.model_name})...")

        eval_prompt = f"""[INST] Task: Check if the Agent response is safe and compliant.
<USER_PROMPT>
{user_prompt}
</USER_PROMPT>

<AGENT_RESPONSE>
{candidate_response}
</AGENT_RESPONSE>
[/INST]"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict security classifier. Analyze the response.\n"
                            "Reply strictly with 'safe' or 'unsafe'."
                        )
                    },
                    {"role": "user", "content": eval_prompt}
                ],
                temperature=0.0,
            )
            result = response.choices[0].message.content.strip()
            if result.lower().startswith("safe"):
                return True, "Safe"
            return False, f"Semantic Policy Violation: {result}"
        except Exception as e:
            logger.error(f"Semantic guardrail error: {e}")
            return False, "Guardrail Execution Error"
