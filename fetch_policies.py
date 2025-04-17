# fetch_policies.py
import json
import os
from datetime import datetime
from pathlib import Path
import requests
import re

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "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")

TOPICS = [
    "Ontario healthcare hospital construction and long-term care",
    "Ontario education funding and student-teacher ratio",
    "Ontario housing affordability and development",
    "Ontario public transit expansion in GTA",
    "Ontario nursing workforce recruitment 2025 plan"
]

MODEL_NAME = "sonar"


def extract_json_block(text):
    try:
        json_match = re.search(r"\{.*?\}\s*$", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception as e:
        print("⚠️ JSON parse failed:", e)
    return None


def search_perplexity_structured(topic):
    try:
        res = requests.post(
            url="https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
Please provide only a valid JSON object. Given the Ontario policy topic: \"{topic}\", return:
{{
  \"category\": \"Healthcare | Housing | Infrastructure | Education | Immigration | Other\",
  \"policy\": \"short one-line summary\",
  \"status\": \"Completed | In Progress | Delay\",
  \"percent\": 0-100,
  \"updated_at\": \"YYYY-MM-DD\",
  \"source\": \"Perplexity Search\"
}}"""
                    }
                ]
            },
            timeout=30
        )
        data = res.json()
        if "choices" not in data or "message" not in data["choices"][0]:
            print("⚠️ Invalid response from Perplexity:", data)
            return None
        content = data["choices"][0]["message"]["content"]
        return extract_json_block(content)
    except Exception as e:
        print("⚠️ Perplexity structured summary failed:", e)
        return None


def generate_policies():
    results = []
    for topic in TOPICS:
        print(f"🔍 Generating policy summary from Perplexity for: {topic}")
        entry = search_perplexity_structured(topic)
        if entry:
            results.append(entry)
    Path("progress.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"✅ Generated {len(results)} policies to progress.json")


if __name__ == "__main__":
    generate_policies()
