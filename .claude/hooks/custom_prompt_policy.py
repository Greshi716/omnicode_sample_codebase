"""
Custom Project UserPromptSubmit Hook: Lending System Policy.
Enforces local project guidelines (e.g. blocking customer credit card numbers or PII)
without modifying the sovereign Base OmniCode SDD Plugin.
"""
import sys
import json
import re

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = payload.get("prompt", "")

# Check for raw credit card numbers or simulated payment PII in user queries
CREDIT_CARD_REGEX = r"\b(?:\d{4}[ -]?){3}\d{4}\b"
if re.search(CREDIT_CARD_REGEX, prompt):
    print("Blocked by Custom Project Hook: Sensitive payment data detected in prompt.", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
