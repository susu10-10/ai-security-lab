import os
import sys
from llm_app import generate_response
from policy import evaluate, load_policy_config

SAFE_DIR = "samples/safe"
UNSAFE_DIR = "samples/unsafe"
CONFIG = load_policy_config()

def run_directory(directory, expect_pass):
    errors = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath) as f:
            prompt = f.read().strip()
        output = generate_response(prompt)
        result = evaluate(prompt, output, CONFIG)
        status = "PASS" if result["passed"] else "BLOCK"
        print(f"[{expect_pass and 'SAFE' or 'UNSAFE'}] {filename}: {status}")
        if expect_pass and not result["passed"]:
            errors.append(f"Safe sample {filename} was blocked")
        if not expect_pass and result["passed"]:
            errors.append(f"Unsafe sample {filename} was NOT blocked (bypass)")
    return errors

def main():
    all_errors = []
    all_errors += run_directory(SAFE_DIR, expect_pass=True)
    all_errors += run_directory(UNSAFE_DIR, expect_pass=False)
    if all_errors:
        print("\n❌ Errors:")
        for e in all_errors:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("\n✅ All samples behaved as expected.")
        sys.exit(0)

if __name__ == "__main__":
    main()