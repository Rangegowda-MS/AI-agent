import json
import os

from openai import OpenAI


# =========================================================
# OPENAI CLIENT
# =========================================================

def _get_client():
    """
    Create and return an OpenAI client using the API key
    stored in the environment.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. "
            "Add OPENAI_API_KEY=your_key_here to your .env file."
        )

    return OpenAI(api_key=api_key)


# =========================================================
# SAFE INTEGER
# =========================================================

def safe_integer(value):
    """
    Safely convert a value to a non-negative integer.
    Handles values such as:
        5000
        "5000"
        "₹5,000"
        "5,000"
        None
        ""
    """

    if value is None:
        return 0

    try:
        if isinstance(value, str):
            value = (
                value
                .replace("₹", "")
                .replace(",", "")
                .strip()
            )

        return max(0, int(float(value)))

    except (ValueError, TypeError):
        return 0


# =========================================================
# BUILD TRIP PLAN
# =========================================================

def build_trip_plan(
    destination,
    days,
    travelers,
    budget,
    interests="",
    hotel_style="Budget",
):
    """
    Generate a personalized AI travel itinerary.
    """

    client = _get_client()

    # -----------------------------------------------------
    # CLEAN INPUTS
    # -----------------------------------------------------

    destination = str(destination).strip()

    days = max(
        1,
        min(
            safe_integer(days),
            30
        )
    )

    travelers = max(
        1,
        min(
            safe_integer(travelers),
            20
        )
    )

    budget = max(
        0,
        safe_integer(budget)
    )

    interests = str(
        interests or "General sightseeing"
    ).strip()

    hotel_style = str(
        hotel_style or "Budget"
    ).strip()


    # -----------------------------------------------------
    # AI PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are Voyage AI, a professional AI travel planning assistant.

Create a realistic and personalized travel itinerary.

TRIP DETAILS

Destination: {destination}
Number of days: {days}
Number of travelers: {travelers}
Total user budget in INR: ₹{budget}
Interests: {interests}
Hotel style: {hotel_style}

IMPORTANT BUDGET REQUIREMENTS

The user has explicitly provided a total budget of ₹{budget}.

You MUST create a realistic estimated budget for the trip.

The budget_analysis values MUST NOT be zero unless that
category genuinely costs nothing.

The following categories must be estimated:

- accommodation
- transportation
- food
- activities
- miscellaneous

The sum of the budget_analysis categories should be
approximately equal to estimated_total_cost.

estimated_total_cost must be greater than 0 when the
user budget is greater than 0.

Do NOT simply return zero values.

Use realistic Indian travel estimates.

Consider:

- number of travelers
- number of days
- destination
- hotel style
- transportation requirements
- food
- sightseeing/activity costs
- miscellaneous expenses

The estimated trip cost should normally remain within
the user's budget when the budget is reasonable.

If the provided budget is unusually low for the destination,
provide the closest realistic estimate and mention the
budget limitation in the summary or tips.

Do not claim that you checked live hotel prices,
flight prices, availability, or real-time booking systems.

All costs are estimates.

IMPORTANT ITINERARY REQUIREMENTS

1. Create exactly {days} itinerary days.
2. Consider {travelers} travelers.
3. Personalize the itinerary based on:
   {interests}
4. Include morning, afternoon and evening activities.
5. Avoid unrealistic distances.
6. Group nearby attractions together.
7. Avoid repeating the same activity unnecessarily.
8. Include practical travel suggestions.
9. Include well-known attractions and some unique experiences.
10. Use Indian Rupees for all costs.

IMPORTANT DAY COST REQUIREMENTS

Every itinerary day MUST have a realistic estimated_cost.

The sum of all itinerary day estimated_cost values should
approximately match the estimated_total_cost.

Do NOT return 0 for every day.

If the trip budget is ₹{budget}, distribute the estimated
trip cost across the itinerary realistically.

RETURN ONLY JSON.

The response MUST follow exactly this structure:

{{
    "destination": "{destination}",

    "summary": "Short personalized description of the trip",

    "estimated_total_cost": 25000,

    "currency": "INR",

    "budget_analysis": {{
        "accommodation": 8000,
        "transportation": 5000,
        "food": 5000,
        "activities": 5000,
        "miscellaneous": 2000
    }},

    "itinerary": [
        {{
            "day_number": 1,
            "title": "Day title",
            "morning": "Morning plan",
            "afternoon": "Afternoon plan",
            "evening": "Evening plan",
            "estimated_cost": 5000
        }}
    ],

    "tips": [
        "Useful travel tip"
    ],

    "packing_list": [
        "Item to pack"
    ]
}}

Return exactly {days} objects inside the itinerary array.

Do not use Markdown.
Do not use code fences.
Do not write explanations outside the JSON.

Return ONLY JSON.
"""


    # =====================================================
    # CALL OPENAI
    # =====================================================

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Voyage AI, a professional AI "
                        "travel planning assistant. "
                        "Always return valid JSON. "
                        "Never return zero budget values when "
                        "a positive user budget is provided."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.7,
        )

    except Exception as exc:

        raise RuntimeError(
            f"Unable to contact the AI service: {exc}"
        ) from exc


    # =====================================================
    # GET RESPONSE
    # =====================================================

    content = response.choices[0].message.content

    if not content:

        raise RuntimeError(
            "The AI returned an empty response."
        )

    content = content.strip()


    # =====================================================
    # REMOVE MARKDOWN FENCES
    # =====================================================

    if content.startswith("```"):

        if content.startswith("```json"):
            content = content[7:]

        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()


    # =====================================================
    # PARSE JSON
    # =====================================================

    try:

        result = json.loads(content)

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            f"AI returned invalid JSON: {exc}"
        ) from exc


    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if not isinstance(result, dict):

        raise RuntimeError(
            "AI response must be a JSON object."
        )


    if "itinerary" not in result:

        raise RuntimeError(
            "AI response does not contain an itinerary."
        )


    if not isinstance(
        result["itinerary"],
        list
    ):

        raise RuntimeError(
            "AI itinerary has an invalid format."
        )


    # =====================================================
    # NORMALIZE ITINERARY
    # =====================================================

    itinerary = result["itinerary"]

    if len(itinerary) != days:

        raise RuntimeError(
            f"AI returned {len(itinerary)} itinerary days "
            f"instead of the requested {days}."
        )


    cleaned_itinerary = []


    for index, day in enumerate(
        itinerary,
        start=1
    ):

        if not isinstance(day, dict):

            raise RuntimeError(
                f"Invalid itinerary data for day {index}."
            )


        cleaned_day = {

            "day_number": index,

            "title": str(
                day.get(
                    "title",
                    f"Day {index}"
                )
            ),

            "morning": str(
                day.get(
                    "morning",
                    ""
                )
            ),

            "afternoon": str(
                day.get(
                    "afternoon",
                    ""
                )
            ),

            "evening": str(
                day.get(
                    "evening",
                    ""
                )
            ),

            "estimated_cost": safe_integer(
                day.get(
                    "estimated_cost",
                    0
                )
            ),
        }


        cleaned_itinerary.append(
            cleaned_day
        )


    result["itinerary"] = cleaned_itinerary


    # =====================================================
    # NORMALIZE BUDGET ANALYSIS
    # =====================================================

    budget_analysis = result.get(
        "budget_analysis",
        {}
    )


    if not isinstance(
        budget_analysis,
        dict
    ):

        budget_analysis = {}


    accommodation = safe_integer(
        budget_analysis.get(
            "accommodation",
            0
        )
    )

    transportation = safe_integer(
        budget_analysis.get(
            "transportation",
            0
        )
    )

    food = safe_integer(
        budget_analysis.get(
            "food",
            0
        )
    )

    activities = safe_integer(
        budget_analysis.get(
            "activities",
            0
        )
    )

    miscellaneous = safe_integer(
        budget_analysis.get(
            "miscellaneous",
            0
        )
    )


    # =====================================================
    # CALCULATE BUDGET TOTAL
    # =====================================================

    budget_breakdown_total = (
        accommodation
        + transportation
        + food
        + activities
        + miscellaneous
    )


    # =====================================================
    # CALCULATE ITINERARY TOTAL
    # =====================================================

    itinerary_total = sum(
        safe_integer(
            day.get(
                "estimated_cost",
                0
            )
        )
        for day in cleaned_itinerary
    )


    # =====================================================
    # DETERMINE FINAL TOTAL
    # =====================================================

    ai_total = safe_integer(
        result.get(
            "estimated_total_cost",
            0
        )
    )


    if ai_total > 0:

        estimated_total_cost = ai_total

    elif budget_breakdown_total > 0:

        estimated_total_cost = (
            budget_breakdown_total
        )

    elif itinerary_total > 0:

        estimated_total_cost = (
            itinerary_total
        )

    elif budget > 0:

        # Last-resort fallback.
        # If the AI failed to provide any cost,
        # use the user's budget as the estimated
        # trip cost instead of displaying ₹0.
        estimated_total_cost = budget

    else:

        estimated_total_cost = 0


    # =====================================================
    # FIX EMPTY BUDGET BREAKDOWN
    # =====================================================

    if budget > 0 and budget_breakdown_total == 0:

        estimated_total_cost = max(
            estimated_total_cost,
            itinerary_total,
            1
        )


        # Create a practical fallback breakdown.

        accommodation = round(
            estimated_total_cost * 0.30
        )

        transportation = round(
            estimated_total_cost * 0.20
        )

        food = round(
            estimated_total_cost * 0.20
        )

        activities = round(
            estimated_total_cost * 0.20
        )

        miscellaneous = (
            estimated_total_cost
            - accommodation
            - transportation
            - food
            - activities
        )


    # =====================================================
    # NORMALIZE BREAKDOWN
    # =====================================================

    result["budget_analysis"] = {

        "accommodation":
            accommodation,

        "transportation":
            transportation,

        "food":
            food,

        "activities":
            activities,

        "miscellaneous":
            miscellaneous,
    }


    result["estimated_total_cost"] = (
        estimated_total_cost
    )

    result["currency"] = "INR"


    # =====================================================
    # NORMALIZE TIPS
    # =====================================================

    tips = result.get(
        "tips",
        []
    )


    if not isinstance(
        tips,
        list
    ):

        tips = []


    result["tips"] = [
        str(tip)
        for tip in tips
    ]


    # =====================================================
    # NORMALIZE PACKING LIST
    # =====================================================

    packing_list = result.get(
        "packing_list",
        []
    )


    if not isinstance(
        packing_list,
        list
    ):

        packing_list = []


    result["packing_list"] = [
        str(item)
        for item in packing_list
    ]


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return result