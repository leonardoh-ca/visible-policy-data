# fetch_policies.py
import json
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup


def fetch_ontario_newsroom():
    url = "https://news.ontario.ca/en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select(".release-listing .release-card")[:5]
    data = []
    for article in articles:
        title = article.select_one(".release-title").get_text(strip=True)
        date = article.select_one(".release-date").get_text(strip=True)
        href = article.select_one("a")['href']
        link = f"https://news.ontario.ca{href}" if href.startswith("/") else href
        data.append({
            "category": "Ontario Government",
            "policy": title,
            "status": "In Progress",
            "percent": 10,
            "updated_at": f"{date} (Scraped)",
            "source": link
        })
    return data


def fetch_canada_newsroom():
    url = "https://www.canada.ca/en/news.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select(".wb-news .row")[:5]
    data = []
    for article in articles:
        link_tag = article.select_one("a")
        title = link_tag.get_text(strip=True)
        href = link_tag['href']
        link = f"https://www.canada.ca{href}" if href.startswith("/") else href
        date = article.select_one("time")
        date_text = date.get("datetime") if date else "Unknown"
        data.append({
            "category": "Canada Federal",
            "policy": title,
            "status": "In Progress",
            "percent": 5,
            "updated_at": f"{date_text} (Scraped)",
            "source": link
        })
    return data


def consolidate():
    data = fetch_ontario_newsroom() + fetch_canada_newsroom()
    Path("progress.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"✅ Updated progress.json with {len(data)} records")


if __name__ == "__main__":
    consolidate()
