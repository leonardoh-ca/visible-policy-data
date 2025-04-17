# fetch_policies.py
import json
from datetime import datetime, timezone
from pathlib import Path

# 假数据（示例结构，后面会替换为爬虫结果）
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")

policies = [
    {
        "category": "Healthcare",
        "policy": "Build 50 hospitals & 58,000 LTC beds",
        "status": "In Progress",
        "percent": 36,
        "updated_at": now
    },
    {
        "category": "Workforce",
        "policy": "Hire 30,000 nurses & expand med school seats",
        "status": "In Progress",
        "percent": 40,
        "updated_at": now
    },
    {
        "category": "Infrastructure",
        "policy": "Invest $200B in transit & housing",
        "status": "Completed",
        "percent": 100,
        "updated_at": now
    },
    {
        "category": "Efficiency",
        "policy": "Cut red tape $1B, fast permitting",
        "status": "Delay",
        "percent": 75,
        "updated_at": now
    },
    {
        "category": "Primary Care",
        "policy": "Universal access to family doctors by 2029",
        "status": "In Progress",
        "percent": 20,
        "updated_at": now
    }
]

# 输出为 JSON 文件
Path("progress.json").write_text(
    json.dumps(policies, indent=2), encoding="utf-8"
)

print("✅ progress.json updated at", now)
