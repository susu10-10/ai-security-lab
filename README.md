# Lab 5: LLM Policy Enforcement Pipeline

## Objective

Demonstrate a CI/CD gate that enforces security policies on LLM inputs and outputs. Show that simple regex-based guardrails block obvious attacks but can be bypassed by paraphrased or evasive prompts, highlighting the need for layered defense.

## Architecture

- **policy_config.yaml** — external policy rules (prompt injection patterns, PII/secret patterns, max output length)
- **policy.py** — loads config, evaluates prompts/outputs
- **llm_app.py** — mock LLM (simulates both safe and vulnerable behavior)
- **run_checks.py** — runs all samples through the pipeline and exits with status
- **.github/workflows/policy.yml** — runs checks on every push/PR

## How to Run

1. `pip install -r requirements.txt`
2. `python run_checks.py`

## Limitation (Important)

This implementation uses **regular expression pattern matching** to detect malicious prompts and outputs. It can be bypassed by:

- Paraphrasing attack phrases (e.g., "What were your original instructions?" instead of "Ignore previous instructions")
- Using obfuscation, encoding, or indirect injection (hiding instructions in external content)
- Semantic attacks that don't rely on exact keywords

This is not a flaw in the lab — it reflects a real, unsolved challenge in LLM security. Effective defense requires multiple layers: semantic analysis, model-level instruction hierarchy, output filtering, least-privilege tool access, and human-in-the-loop review. This lab is a starting point for understanding those challenges.