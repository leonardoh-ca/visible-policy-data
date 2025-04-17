# fetch_policies.py
import json
import os
import re
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
MODEL_NAME = "sonar"

# Load topics.json (fixed structure with category+topic)
with open("topics.json", encoding="utf-8") as f:
    TOPICS = json.load(f)


def extract_json_block(text):
    try:
        match = re.search(r"\{.*?\}\s*$", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
    except Exception as e:
        print("⚠️ JSON parse failed:", e)
    return None


def ask_perplexity(topic):
    try:
        prompt = f"""
You are an assistant tracking Ontario government policy.

Given the policy topic: \"{topic}\", summarize its current implementation status based on current information from credible sources. Respond ONLY in this exact JSON format:

{{
  "status": "Completed" | "In Progress" | "Delay",
  "percent": number (0 to 100),
  "updated_at": "YYYY-MM-DD",
  "source": "a valid URL starting with https:// from a real news site that confirms this policy update"
}}

Return ONLY this JSON, nothing else.
"""

        res = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        data = res.json()
        content = data["choices"][0]["message"]["content"]
        return extract_json_block(content)
    except Exception as e:
        print(f"⚠️ Failed to fetch Perplexity summary: {e}")
        return None


def generate_progress():
    results = []
    for item in TOPICS:
        print(f"🔍 Asking Perplexity for: {item['topic']}")
        details = ask_perplexity(item["topic"])
        if details:
            results.append({
                "category": item["category"],
                "policy": item["topic"],
                "status": details.get("status", "In Progress"),
                "percent": details.get("percent", 0),
                "updated_at": details.get("updated_at", datetime.now().strftime("%Y-%m-%d")),
                "source": details.get("source", "https://www.ontario.ca/news")
            })
    Path("progress.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"✅ {len(results)} entries written to progress.json")


if __name__ == "__main__":
    generate_progress()
