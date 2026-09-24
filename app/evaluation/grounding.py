import json
import re

from ollama import chat


MODEL = "qwen2.5-coder:7b"


def build_grounding_prompt(
    claim: str,
    context: str
):
    return f"""
You are evaluating whether a claim is supported by retrieved document context.

Your task is NOT to decide whether the claim is generally true.

Your task is only to determine whether the provided context
contains enough information to support the claim.

Rules:
- Return SUPPORTED if the context directly supports the claim.
- Return NOT_SUPPORTED if the context does not support the claim.
- Do not use outside knowledge.
- Do not infer information that is not present in the context.
- Ignore whether the claim sounds reasonable.
- Evaluate only the relationship between the claim and the context.

Return ONLY valid JSON in this exact format:

{{
    "verdict": "SUPPORTED",
    "reason": "short explanation"
}}

Claim:
{claim}

Context:
{context}
""".strip()


def parse_evaluation_response(
    content: str
):
    content = content.strip()

    # First attempt: response is already valid JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Second attempt: remove markdown code fences
    content = re.sub(
        r"```(?:json)?",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = content.replace(
        "```",
        ""
    ).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Third attempt: extract the JSON object
    match = re.search(
        r"\{.*\}",
        content,
        re.DOTALL
    )

    if match:
        try:
            return json.loads(
                match.group(0)
            )
        except json.JSONDecodeError:
            pass

    return None


def evaluate_claim(
    claim: str,
    context: str
):
    prompt = build_grounding_prompt(
        claim,
        context
    )

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    content = response.message.content.strip()

    result = parse_evaluation_response(
        content
    )

    if result is None:
        return {
            "verdict": "INVALID",
            "reason": (
                "Evaluator returned an "
                "unparseable response."
            )
        }

    verdict = result.get(
        "verdict",
        "INVALID"
    )

    reason = result.get(
        "reason",
        ""
    )

    if verdict not in {
        "SUPPORTED",
        "NOT_SUPPORTED"
    }:
        verdict = "INVALID"

    return {
        "verdict": verdict,
        "reason": reason
    }