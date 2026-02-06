import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def rule_based_extraction(text):
    fields = {}

    # Policy number
    match = re.search(r"POLICY NUMBER[:\s]*([A-Z0-9\-]+)", text, re.IGNORECASE)
    if match:
        fields["policyNumber"] = match.group(1)

    # Policyholder name
    match = re.search(r"NAME OF INSURED.*?:\s*(.+)", text, re.IGNORECASE)
    if match:
        fields["policyholderName"] = match.group(1)

    # Date of loss
    match = re.search(r"DATE OF LOSS.*?(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)
    if match:
        fields["incidentDate"] = match.group(1)

    # Location
    match = re.search(r"LOCATION OF LOSS[:\s]*([A-Za-z0-9, \-]+)", text, re.IGNORECASE)
    if match:
        location = match.group(1).strip()
        if len(location) < 80:  # avoid long garbage text
            fields["incidentLocation"] = location

    # Estimated damage
    match = re.search(r"ESTIMATE AMOUNT[:\s]*\$?([\d,]+)", text, re.IGNORECASE)
    if match:
        fields["estimatedDamage"] = int(match.group(1).replace(",", ""))

    # Claim type detection (simple keyword logic)
    if "injury" in text.lower():
        fields["claimType"] = "injury"
    elif "vehicle" in text.lower() or "automobile" in text.lower():
        fields["claimType"] = "vehicle"

    # Description
    match = re.search(r"DESCRIPTION.*?:\s*(.+)", text, re.IGNORECASE)
    if match:
        fields["description"] = match.group(1)

    return fields

def extract_fields_with_ai(text):
    # If no API key, use fallback
    if not client:
        return rule_based_extraction(text)

    try:
        prompt = f"""
Extract claim data from this document.
Return only JSON.

{text}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Extract structured insurance claim data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception:
        # Fallback if API fails
        return rule_based_extraction(text)
