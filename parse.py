import json

def parse_json_response(response_text):
    """Strip stray markdown fences (if any) and parse the model's response text as JSON."""
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
    return json.loads(cleaned)
