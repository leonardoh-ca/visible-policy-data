# fetch_policies.py
import json
import re
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
import requests


def classify_category(text):
    text = text.lower()
    if any(word in text for word in ["hospital", "nurse", "health"]):
        return "Healthcare"
    elif any(word in text for word in ["transit", "infrastructure", "highway", "subway"]):
        return "Infrastructure"
    elif any(word in text for word in ["housing", "home", "rent", "shelter"]):
        return "Housing"
    elif any(word in text for word in ["school", "education", "student", "teacher"]):
        return "Education"
    elif any(word in text for word in ["immigration", "refugee", "visa"]):
        return "Immigration"
    return "General"


def extract_status_percent(text):
    text = text.lower()
    if "completed" in text:
        return ("Completed", 100)
    elif any(w in text for w in ["launched", "started", "in progress"]):
        return ("In Progress", 50)
    elif any(w in text for w in ["announced", "planned"]):
        return ("In Progress", 10)
    elif "delayed" in text:
        return ("Delay", 70)
    return ("In Progress", 5)


def fetch_rss_ontario_newsroom():
    rss_url = "https://news.ontario.ca/newsroom/en/rss"
    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Failed to fetch RSS feed: {e}")
        return []

    root = ET.fromstring(response.content)
    items = root.findall(".//item")[:5]
    data = []

    for item in items:
        try:
            title = item.findtext("title", default="")
            link = item.findtext("link", default="")
            description = item.findtext("description", default="")
            pub_date = item.findtext("pubDate", default="Unknown")

            category = classify_category(title + description)
            status, percent = extract_status_percent(description)

            data.append({
                "category": category,
                "policy": title,
                "status": status,
                "percent": percent,
                "updated_at": pub_date,
                "source": link
            })
        except Exception as e:
            print(f"⚠️ Error parsing RSS item: {e}")

    return data


def consolidate():
    all_data = fetch_rss_ontario_newsroom()
    Path("progress.json").write_text(json.dumps(all_data, indent=2), encoding="utf-8")
    print(f"✅ Updated progress.json with {len(all_data)} records")


if __name__ == "__main__":
    consolidate()
