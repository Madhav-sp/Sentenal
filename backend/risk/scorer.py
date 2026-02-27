def calculate_risk(subdomain):
    score = 10

    if "dev" in subdomain or "test" in subdomain:
        score += 40

    if "api" in subdomain:
        score += 20

    if score > 70:
        severity = "HIGH"
    elif score > 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return score, severity