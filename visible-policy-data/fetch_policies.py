import json
from datetime import datetime

data = [
    {
        "category": "Healthcare",
        "policy": "Build 50 hospitals & 58,000 LTC beds",
        "status": "In Progress",
        "percent": 36,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "category": "Workforce",
        "policy": "Hire 30,000 nurses & med school expansion",
        "status": "In Progress",
        "percent": 40,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "category": "Infrastructure",
        "policy": "Invest $200B in transit & housing",
        "status": "Completed",
        "percent": 100,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "category": "Efficiency",
        "policy": "Cut red tape $1B, fast permitting",
        "status": "Delay",
        "percent": 75,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "category": "Primary Care",
        "policy": "Universal access to family doctor by 2029",
        "status": "In Progress",
        "percent": 20,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
]

with open("progress.json", "w") as f:
    json.dump(data, f, indent=2)
