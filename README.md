# Simple Prompt Injection & LLM Policy Enforcement Pipeline

[![Simple LLM Policy Checks](https://github.com/susu10-10/ai-security-lab/actions/workflows/policy.yml/badge.svg)](https://github.com/susu10-10/ai-security-lab/actions/workflows/policy.yml)

## Objectives

Hands-on experiments for learning AI security, focusing on LLM prompt injection and policy enforcement, highlighting the need for layered defense. This repository contains two labs:

1. Prompt injection against a real local LLM that demonstrates why LLMs leak secrets when prompted.

2. Policy enforcement pipeline that builds a regex-based CI gate and shows why it can be bypassed.

Together they demonstrate the need for layered AI security.


## Lab 1: Basic Prompt Injection

### Objective

Demonstrates direct prompt injection against a locally running LLM (via `Ollama`). Uses a red-team script to send various attack prompts and log which ones successfully leak a secret key. Show that a local LLM can be tricked into revealing a secret via multiple prompt injection techniques, and that some attacks bypass simple keyword filters.

### Requirements

- Python 3.10+
- Ollama (https://ollama.com)
- A small model pulled: `ollama pull phi3:mini` (or `tinyllama`)

### How to Run

    ```bash
    cd prompt_injection
    pip install -r requirements.txt
    python red_t.py
    ```
> Results are saved to `results.json` and `results.csv`. Examine which attacks leaked the secret (SK-123456).

### Key Findings (Sample)

- Direct override and persona change often succeed.

- Obfuscation and few-shot manipulation do not rely on literal keywords like “ignore previous instructions.” A simple keyword filter (as implemented in Lab 2) would likely miss them.

- The benign prompt does not leak.

- This demonstrates that real LLMs are vulnerable to injection, and that regex-based guardrails (like in Lab 5) are insufficient because they miss paraphrased or obfuscated attacks.

## Lab 2: Policy Enforcement Pipeline

### Objective

Build an automated policy gate that scans LLM inputs/outputs for security violations. Show that while it blocks obvious attacks, it is bypassed by evasive prompts, highlighting the need for layered defense. Implements a CI/CD gate that enforces regex-based policies on LLM inputs/outputs. Includes both literal and evasive malicious samples to demonstrate the limitations of keyword blocklists.


### Architecture

- **policy_config.yaml** external policy rules (prompt injection patterns, PII/secret patterns, max output length)
- **policy.py** loads config, evaluates prompts/outputs
- **llm_app.py** mock LLM (simulates both safe and vulnerable behavior)
- **run_checks.py** runs all samples through the pipeline and exits with status
- **.github/workflows/policy.yml** runs checks on every push/PR

### How to Run

1. `pip install -r requirements.txt`
2. `python run_checks.py`

> The script will fail because the evasive malicious samples bypass the policy (by design). This illustrates the limitation.

### Limitation

This implementation uses **regular expression pattern matching** to detect malicious prompts and outputs. It can be bypassed by:

- Paraphrasing attack phrases (e.g., "What were your original instructions?" instead of "Ignore previous instructions")
- Using obfuscation (e.g., leetspeak, encoding) or indirect injection (hiding instructions in external content)
- Semantic attacks that don't rely on exact keywords


>Why the CI is red: run_checks.py is designed to fail when an unsafe sample is not blocked. The evasive malicious samples intentionally bypass the regex policies, so the pipeline fails. This is the expected outcome and demonstrates the limitation of keyword-based guardrails.

>This is not a flaw in the lab, it reflects a real, unsolved challenge in LLM security. Effective defense requires multiple layers: semantic analysis, model-level instruction hierarchy, output filtering, least-privilege tool access, and human-in-the-loop review. This lab is a starting point for understanding those challenges.
