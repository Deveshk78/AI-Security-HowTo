# AI Security Demo Project Documentation

## Copyright
© 2026 Devesh Kumar
Email: devesh2178@gmail.com

All content in this project, including architecture diagrams, call flow documentation, guardrail notes, source code, and project documentation, is protected by copyright and may not be redistributed, republished, or used in commercial or non-commercial materials without explicit written permission from the copyright holder.

---

## Project Overview
This project demonstrates a layered AI security architecture for processing untrusted user input with local large language models. It is designed to show how a system can reduce prompt injection risk by separating raw user content from trusted reasoning tasks.

The implementation uses:
- a local Ollama-backed LLM environment
- a strict untrusted extraction step
- a trusted execution phase
- deterministic regex guardrails
- semantic safety classification

---

## Core Design Goals
1. Treat all untrusted text as hostile input.
2. Prevent prompt injection before the model executes.
3. Extract only structured data from raw payloads.
4. Restrict the trusted model to sanitized schema-based context.
5. Validate both input and output using security checks.
 
---

## System Components

### 1. Main Orchestrator
The orchestrator is implemented in `main.py` and coordinates the full pipeline.
It performs the following actions:
- loads the environment configuration
- checks raw input with the deterministic input guardrail
- initializes the local OpenAI-compatible client to Ollama
- runs the untrusted extraction step
- executes the trusted task
- verifies output with regex and semantic guardrails

### 2. Dual-LLM Pipeline
The dual-model design is implemented in `security/dual_llm.py`.

- `extract_untrusted_data(...)`: parses raw text into a structured schema, treating embedded instructions as passive data only.
- `execute_trusted_task(...)`: reasons over sanitized JSON and the user goal, isolating the final answer from attacker-controlled instructions.

### 3. Guardrail Layer
The guardrail logic is implemented in `security/guardrails.py`.

It includes:
- `RegexGuardrail.validate_input(...)`: blocks malicious raw input before the model call
- `RegexGuardrail.validate(...)`: checks candidate output for prompt leaks, secrets, financial abuse, and commands
- `SemanticGuardrail.validate_output(...)`: uses a second model pass to evaluate output compliance

---

## Example Attack Scenario
The current demo includes a malicious email that contains instructions such as:
- ignore previous instructions
- reveal the system prompt
- trigger a fake financial action
- attempt to exfiltrate hidden secrets

The pipeline is built to block this payload before it reaches the trusted model and also to reject unsafe candidate responses before they are returned to the user.

---

## File Structure
- `main.py` — entry point and orchestration flow
- `security/dual_llm.py` — dual-model logic and sanitization
- `security/guardrails.py` — input/output guardrails
- `docs/architecture_diagram.png` — architecture overview
- `docs/call_flow_diagram.png` — sequence call flow
- `docs/guardrail_activity_diagram.png` — guardrail activity logic
- `docs/PROJECT_DOCUMENTATION.md` — this document

---

## Diagram Assets
The following diagram files are available under the project `docs` folder:
- architecture_diagram.png
- call_flow_diagram.png
- guardrail_activity_diagram.png

These are intended for future reference, presentations, research notes, and internal documentation.

---

## Notes for Future Work
Recommended next steps:
- add structured policy-as-code definitions
- expand regex coverage for novel prompt injections
- create adversarial test cases for prompt override variations
- add logging and alerting for blocked requests
- integrate stricter schema validation and allowlists

---

## Contact
Devesh Kumar
Email: devesh2178@gmail.com
