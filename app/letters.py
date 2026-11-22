"""Decline letters: an AI model drafts the letter from the reason codes; a person in lending signs it off."""
import anthropic

from .reasons import REASON_TEXT

client = anthropic.Anthropic()

MODEL = "claude-sonnet-4-5-20250929"


def draft_decline_letter(applicant_name: str, reason_codes: list[str]) -> str:
    reasons = "\n".join(f"- {REASON_TEXT[c]}" for c in reason_codes)
    msg = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": (
            f"Write a short, plain-English letter to {applicant_name} saying their personal loan application was "
            f"declined, giving these reasons and how to ask for a review by a person:\n{reasons}")}],
    )
    return msg.content[0].text
