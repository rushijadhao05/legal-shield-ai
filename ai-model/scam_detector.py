from typing import Dict, List

SCAM_RULES = [
    {
        "keyword": "otp",
        "status": "Potential Scam Detected",
        "threat_type": "OTP Fraud",
        "severity": "High",
        "law": "IT Act Section 66C, Section 66D",
        "advice": "Never share OTP with anyone. This may be fraud or identity theft."
    },
    {
        "keyword": "password",
        "status": "Potential Scam Detected",
        "threat_type": "Credential Theft",
        "severity": "High",
        "law": "IT Act Section 43, Section 66C",
        "advice": "Do not share your password. Change it immediately if already shared."
    },
    {
        "keyword": "bank",
        "status": "Potential Scam Detected",
        "threat_type": "Banking Fraud",
        "severity": "High",
        "law": "IT Act Section 66D",
        "advice": "Verify banking messages only from official sources."
    },
    {
        "keyword": "verify account",
        "status": "Potential Scam Detected",
        "threat_type": "Phishing Attempt",
        "severity": "Medium",
        "law": "IT Act Section 66C, Section 66D",
        "advice": "Fake account verification messages are often phishing attempts."
    },
    {
        "keyword": "click now",
        "status": "Potential Scam Detected",
        "threat_type": "Malicious Link",
        "severity": "Medium",
        "law": "IT Act Section 66D",
        "advice": "Avoid clicking unknown links."
    },
    {
        "keyword": "urgent",
        "status": "Potential Scam Detected",
        "threat_type": "Social Engineering",
        "severity": "Medium",
        "law": "IT Act Section 66D",
        "advice": "Scammers create urgency. Verify before acting."
    },
    {
        "keyword": "lottery",
        "status": "Potential Scam Detected",
        "threat_type": "Prize Scam",
        "severity": "Medium",
        "law": "IT Act Section 66D",
        "advice": "Fake lottery messages are common scams."
    },
    {
        "keyword": "gift",
        "status": "Potential Scam Detected",
        "threat_type": "Fake Offer Scam",
        "severity": "Low",
        "law": "IT Act Section 66D",
        "advice": "Be careful with unexpected gift offers."
    }
]


def analyze_text(text: str) -> Dict:
    text_lower = text.lower().strip()
    matched_rules: List[Dict] = []

    for rule in SCAM_RULES:
        if rule["keyword"] in text_lower:
            matched_rules.append(rule)

    if matched_rules:
        severity_rank = {"Low": 1, "Medium": 2, "High": 3}
        highest_severity = "Low"

        for rule in matched_rules:
            if severity_rank[rule["severity"]] > severity_rank[highest_severity]:
                highest_severity = rule["severity"]

        return {
            "status": "Potential Scam Detected",
            "severity": highest_severity,
            "matched_keywords": [rule["keyword"] for rule in matched_rules],
            "threat_types": list({rule["threat_type"] for rule in matched_rules}),
            "applicable_laws": list({rule["law"] for rule in matched_rules}),
            "advice": list({rule["advice"] for rule in matched_rules}),
            "safe": False
        }

    return {
        "status": "Seems Safe",
        "severity": "Low",
        "matched_keywords": [],
        "threat_types": ["No obvious threat detected"],
        "applicable_laws": [],
        "advice": [
            "No major scam keyword detected.",
            "Still verify unknown links, messages, and requests carefully."
        ],
        "safe": True
    }
