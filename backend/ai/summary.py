def generate_summary(assets):
    high = sum(1 for a in assets if a["severity"] == "HIGH")
    medium = sum(1 for a in assets if a["severity"] == "MEDIUM")

    return f"""
Analysis completed.

{high} high-risk assets detected.
{medium} medium-risk services identified.

Development or testing environments may expose internal systems.
Recommendation: restrict public access and enforce authentication.
"""