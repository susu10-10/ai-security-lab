"""Load security policies from YAML and evaluate prompts/outputs."""

import re
import yaml

CONFIG_FILE = "policy_config.yaml"

def load_policy_config(config_path=CONFIG_FILE):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def check_prompt(prompt: str, config: dict) -> list:
    violations = []
    prompt_lower = prompt.lower()
    for pattern in config.get("prompt_injection_patterns", []):
        if re.search(pattern, prompt_lower):
            violations.append(f"Prompt injection pattern detected: '{pattern}'")
    return violations

def check_output(output: str, config: dict) -> list:
    violations = []
    # PII check
    for pattern in config.get("output_pii_patterns", []):
        if re.search(pattern, output):
            violations.append(f"PII pattern detected: '{pattern}'")
    # Secret check
    for pattern in config.get("output_secret_patterns", []):
        if re.search(pattern, output, re.IGNORECASE):
            violations.append(f"Secret pattern detected: '{pattern}'")
    # Length check
    max_len = config.get("max_output_length", 200)
    if len(output) > max_len:
        violations.append(f"Output length {len(output)} exceeds {max_len}")
    return violations

def evaluate(prompt: str, output: str, config: dict = None) -> dict:
    if config is None:
        config = load_policy_config()
    prompt_violations = check_prompt(prompt, config)
    output_violations = check_output(output, config)
    all_violations = prompt_violations + output_violations
    return {
        "prompt": prompt,
        "output": output,
        "violations": all_violations,
        "passed": len(all_violations) == 0,
    }