MANDATORY_FIELDS = [
    "policyNumber",
    "incidentDate",
    "estimatedDamage",
    "claimType"
]

def detect_missing(fields):
    missing = []
    for field in MANDATORY_FIELDS:
        if field not in fields or not fields[field]:
            missing.append(field)
    return missing


def route_claim(fields, missing):
    description = str(fields.get("description", "")).lower()
    damage = fields.get("estimatedDamage", 0)
    claim_type = str(fields.get("claimType", "")).lower()

    if missing:
        return "Manual Review", "Mandatory fields missing"

    if any(word in description for word in ["fraud", "inconsistent", "staged"]):
        return "Investigation Flag", "Fraud-related keywords detected"

    if claim_type == "injury":
        return "Specialist Queue", "Injury claim"

    if isinstance(damage, (int, float)) and damage < 25000:
        return "Fast-track", "Damage below threshold"

    return "Manual Review", "Default routing"
