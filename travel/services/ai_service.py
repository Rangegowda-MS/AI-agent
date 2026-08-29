from .travel_data import get_destination

def build_trip_plan(destination, days, travelers, budget, interests, hotel_style):
    places, daily_base, tagline = get_destination(destination)
    multiplier = {"Budget": .8, "Comfort": 1.0, "Luxury": 1.5}.get(hotel_style, 1.0)
    total = round(daily_base * days * multiplier + 2500 * max(travelers - 1, 0))
    interest = interests or "local culture, food and sightseeing"
    itinerary = []
    for i in range(days):
        a, b = places[i % len(places)], places[(i + 1) % len(places)]
        itinerary.append({
            "day_number": i + 1,
            "title": f"Day {i+1} • {a}",
            "morning": f"Explore {a} at a relaxed pace.",
            "afternoon": f"Visit {b} and choose activities matching {interest}.",
            "evening": "Enjoy local dinner and an easy evening walk.",
            "estimated_cost": max(500, round(daily_base * multiplier)),
        })
    advice = ("The estimate is above your budget; prefer budget stays and local transport."
              if budget and total > budget else "The estimate fits your stated budget; keep an emergency buffer."
              if budget else "Add a budget for precise optimization.")
    return {"destination": destination, "summary": f"{days}-day {hotel_style.lower()} plan for {travelers} traveler(s). {tagline}",
            "estimated_total": total, "budget_advice": advice, "itinerary": itinerary}
