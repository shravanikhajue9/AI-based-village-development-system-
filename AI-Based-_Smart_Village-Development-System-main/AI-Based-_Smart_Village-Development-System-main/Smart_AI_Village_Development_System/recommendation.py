def get_suggestions(data):

    suggestions = []

    # Literacy
    if data.get("Literacy Rate (%)", 0) < 70:
        suggestions.append("Increase Schools + Digital Education + Skill Centers")

    # Rainfall
    if data.get("Rainfall (mm)", 0) > 900:
        suggestions.append("Grow Sugarcane, Rice, Banana")

    if data.get("Rainfall (mm)", 0) < 500:
        suggestions.append("Grow Millets, Tur, Cotton")

    # Employment
    if data.get("Unemployment Rate (%)", 0) > 20:
        suggestions.append("Start MSME, Dairy, Food Processing Units")

    # Internet
    if data.get("Internet Connectivity", 1) == 0:
        suggestions.append("Install Fiber Internet + CSC Centers")

    # Roads
    if data.get("Road Connectivity", "Good") == "Poor":
        suggestions.append("Improve Roads + Transport System")

    # Health
    if data.get("Number of Healthcare Centers", 0) < 2:
        suggestions.append("Build PHC + Mobile Health Units")

    if not suggestions:
        suggestions.append("Village is performing well, focus on gradual development.")

    return suggestions