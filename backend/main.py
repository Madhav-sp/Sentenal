from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

from database import scans_collection
from recon.enumerator import get_subdomains, resolve_ip
from risk.scorer import calculate_risk
from ai.summary import generate_summary
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class ScanRequest(BaseModel):
    domain: str


@app.post("/scan")
def start_scan(req: ScanRequest):
    domain = req.domain

    subdomains = get_subdomains(domain)

    assets = []

    for sub in subdomains:
        ip = resolve_ip(sub)
        score, severity = calculate_risk(sub)

        assets.append({
            "subdomain": sub,
            "ip": ip,
            "risk": score,
            "severity": severity
        })

    risk_score = sum(a["risk"] for a in assets) // max(len(assets), 1)

    summary = generate_summary(assets)

    scan_id = str(uuid4())

    scans_collection.insert_one({
        "_id": scan_id,
        "domain": domain,
        "assets": assets,
        "risk_score": risk_score,
        "ai_summary": summary,
        "created_at": datetime.utcnow()
    })

    return {"scan_id": scan_id}


@app.get("/result/{scan_id}")
def get_result(scan_id: str):
    result = scans_collection.find_one({"_id": scan_id}, {"_id": 0})
    return result


@app.post("/simulate-attack")
def simulate_attack(scan_id: str):
    scan = scans_collection.find_one({"_id": scan_id})

    narrative = f"""
Step 1: Attacker discovers exposed subdomains.
Step 2: Development environment identified.
Step 3: Attempts credential access via exposed services.
Step 4: Potential lateral movement inside infrastructure.

This demonstrates how exposed assets increase attack risk.
"""

    return {"attack_narrative": narrative}