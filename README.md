# AI Security Pipeline Demonstration

This repository demonstrates an enterprise-grade AI security architecture combining:
1. **Dual-LLM Isolation** (Untrusted Extractor vs. Trusted Executor)
2. **Deterministic Output Guardrails** (Regex pattern matching)
3. **Semantic Output Guardrails** (Safety classifier scanning)

## Setup & Execution Instructions in VS Code

1. Open VS Code and open the `ai_security_demo` directory:
   `File > Open Folder... > ai_security_demo`

2. Open a terminal in VS Code (`Ctrl + ~` or `Cmd + ~`) and create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate