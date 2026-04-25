import json
import re

def parse_llm_output(output: str):
    try:
        # remove markdown wrappers
        cleaned = re.sub(r"```json|```", "", output).strip()

        data = json.loads(cleaned)

        score = data.get("overall_score", 0)

        # normalize (if model returns 0–10 scale)
        if score <= 10:
            score = score * 10

        return score, data

    except Exception:
        return 0, {}