def estimate_budget(destination: str, days: int, vibe: str) -> str:
    """
    Estimates a day-by-day travel budget based on destination cost tier and vibe.
    """

    # Cost tiers per day (in USD) — [food, transport, accommodation, activities]
    city_tiers = {
        "budget": {
            "food": (8, 20),
            "transport": (3, 8),
            "accommodation": (15, 35),
            "activities": (5, 15),
        },
        "moderate": {
            "food": (20, 50),
            "transport": (10, 20),
            "accommodation": (60, 120),
            "activities": (15, 40),
        },
        "expensive": {
            "food": (50, 120),
            "transport": (20, 40),
            "accommodation": (150, 350),
            "activities": (30, 80),
        },
    }

    # Map destinations to cost tiers
    budget_cities = [
        "bangkok", "hanoi", "ho chi minh", "bali", "jakarta",
        "delhi", "mumbai", "kathmandu", "cairo", "istanbul",
        "budapest", "krakow", "lisbon", "mexico city", "lima"
    ]
    expensive_cities = [
        "tokyo", "zurich", "oslo", "copenhagen", "singapore",
        "sydney", "new york", "london", "paris", "dubai",
        "san francisco", "amsterdam", "stockholm", "hong kong"
    ]

    dest_lower = destination.lower()

    if any(city in dest_lower for city in expensive_cities):
        tier = "expensive"
    elif any(city in dest_lower for city in budget_cities):
        tier = "budget"
    else:
        tier = "moderate"

    # Vibe multipliers
    vibe_multipliers = {
        "luxury":      2.0,
        "adventure":   1.2,
        "food":        1.3,
        "culture":     1.1,
        "relaxation":  1.2,
        "budget":      0.7,
    }
    multiplier = vibe_multipliers.get(vibe.lower(), 1.0)

    # Calculate costs
    costs = city_tiers[tier]
    daily_min = sum(v[0] for v in costs.values())
    daily_max = sum(v[1] for v in costs.values())

    daily_min = round(daily_min * multiplier)
    daily_max = round(daily_max * multiplier)

    total_min = daily_min * days
    total_max = daily_max * days

    # Format output
    lines = [
        f"Budget estimate for a {days}-day {vibe} trip to {destination}:",
        f"  City cost tier: {tier.title()}",
        f"  Vibe multiplier: x{multiplier}",
        f"  Daily estimate: ${daily_min} - ${daily_max} per day",
        f"  Breakdown per day:",
        f"    - Food: ${round(costs['food'][0]*multiplier)} - ${round(costs['food'][1]*multiplier)}",
        f"    - Transport: ${round(costs['transport'][0]*multiplier)} - ${round(costs['transport'][1]*multiplier)}",
        f"    - Accommodation: ${round(costs['accommodation'][0]*multiplier)} - ${round(costs['accommodation'][1]*multiplier)}",
        f"    - Activities: ${round(costs['activities'][0]*multiplier)} - ${round(costs['activities'][1]*multiplier)}",
        f"  Total trip estimate: ${total_min} - ${total_max}",
    ]

    return "\n".join(lines)

