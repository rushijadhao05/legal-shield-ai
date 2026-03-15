import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AI_MODEL_DIR = os.path.join(BASE_DIR, "ai-model")
DATABASE_DIR = os.path.join(BASE_DIR, "database")

sys.path.append(AI_MODEL_DIR)
sys.path.append(DATABASE_DIR)

from scam_detector import analyze_text
from db import create_tables, save_complaint, get_all_complaints

app = Flask(__name__)
CORS(app)

create_tables()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "LEGAL SHIELD AI Backend Running",
        "status": "success",
        "port": 7000,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route("/check-scam", methods=["POST"])
def check_scam():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Please provide valid text"}), 400

    result = analyze_text(text)

    return jsonify({
        "input_text": text,
        "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": result
    })


@app.route("/legal-advice", methods=["POST"])
def legal_advice():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Please provide valid text"}), 400

    result = analyze_text(text)

    return jsonify({
        "summary": result["status"],
        "threat_types": result["threat_types"],
        "applicable_laws": result["applicable_laws"],
        "recommended_steps": [
            "Do not reply to the suspicious message.",
            "Do not click unknown links or share OTP/password.",
            "Take screenshots and collect evidence.",
            "Keep sender details, URL, and message content safe.",
            "Report the matter to the cyber crime portal or police."
        ],
        "advice": result["advice"]
    })


@app.route("/generate-complaint", methods=["POST"])
def generate_complaint():
    data = request.get_json()

    required_fields = ["name", "contact", "incident_text"]
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({"error": f"{field} is required"}), 400

    name = data["name"].strip()
    contact = data["contact"].strip()
    incident_text = data["incident_text"].strip()

    analysis = analyze_text(incident_text)

    complaint_id, created_at = save_complaint(
        name=name,
        contact=contact,
        incident_text=incident_text,
        status=analysis["status"],
        severity=analysis["severity"],
        laws=analysis["applicable_laws"]
    )

    complaint_draft = f"""
Cyber Crime Complaint Draft

Name: {name}
Contact: {contact}
Date: {created_at}

Subject: Complaint regarding suspected cyber fraud / online scam

Respected Sir/Madam,

I would like to report a suspected cyber crime incident. The suspicious content is as follows:

"{incident_text}"

System analysis indicates:
- Status: {analysis["status"]}
- Severity: {analysis["severity"]}
- Applicable Laws: {", ".join(analysis["applicable_laws"]) if analysis["applicable_laws"] else "Further review required"}

I request you to kindly investigate this matter and take necessary legal action.

Sincerely,
{name}
    """.strip()

    return jsonify({
        "message": "Complaint draft generated successfully",
        "complaint_id": complaint_id,
        "complaint_draft": complaint_draft
    })


@app.route("/complaints", methods=["GET"])
def complaints():
    all_complaints = get_all_complaints()
    return jsonify({
        "total_complaints": len(all_complaints),
        "complaints": all_complaints
    })


if __name__ == "__main__":
    app.run(debug=True, port=7000)
