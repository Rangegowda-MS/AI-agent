import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Trip, ItineraryDay
from .services.ai_service import build_trip_plan


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(
        request,
        "travel/home.html"
    )


# =========================================================
# PLANNER PAGE
# =========================================================

def planner(request):
    return render(
        request,
        "travel/planner.html"
    )


# =========================================================
# SAFE INTEGER
# =========================================================

def safe_integer(value, default=0):
    try:
        return max(
            0,
            int(float(value))
        )

    except (ValueError, TypeError):
        return default


# =========================================================
# BUILD FALLBACK BUDGET
# =========================================================

def create_budget_breakdown(total_cost):

    total_cost = safe_integer(total_cost)

    if total_cost <= 0:
        return {
            "accommodation": 0,
            "transportation": 0,
            "food": 0,
            "activities": 0,
            "miscellaneous": 0,
        }

    accommodation = round(total_cost * 0.30)
    transportation = round(total_cost * 0.20)
    food = round(total_cost * 0.20)
    activities = round(total_cost * 0.15)

    miscellaneous = (
        total_cost
        - accommodation
        - transportation
        - food
        - activities
    )

    return {
        "accommodation": accommodation,
        "transportation": transportation,
        "food": food,
        "activities": activities,
        "miscellaneous": max(
            0,
            miscellaneous
        ),
    }


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(request):

    if (
        request.user.is_authenticated
        and request.user.is_staff
    ):
        return redirect("admin_dashboard")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            login(
                request,
                user
            )

            return redirect("admin_dashboard")

        messages.error(
            request,
            "Invalid admin username or password."
        )

    return render(
        request,
        "travel/admin_login.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@staff_member_required(
    login_url="/admin-login/"
)
def admin_dashboard(request):

    trips = Trip.objects.all().order_by(
        "-created_at"
    )

    total_trips = trips.count()

    total_travelers = sum(
        trip.travelers or 0
        for trip in trips
    )

    total_budget = (
        trips.aggregate(
            total=Sum("budget")
        ).get("total") or 0
    )

    total_destinations = (
        trips.values("destination")
        .distinct()
        .count()
    )

    recent_trips = trips[:10]

    context = {
        "total_trips": total_trips,
        "total_travelers": total_travelers,
        "total_budget": total_budget,
        "total_destinations": total_destinations,
        "recent_trips": recent_trips,
    }

    return render(
        request,
        "travel/admin_dashboard.html",
        context
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

def admin_logout(request):

    logout(request)

    return redirect("admin_login")


# =========================================================
# AI TRIP GENERATOR API
# =========================================================

@csrf_exempt
@require_POST
def generate_plan(request):

    # -----------------------------------------------------
    # READ JSON
    # -----------------------------------------------------

    try:

        data = json.loads(
            request.body
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON request."
            },
            status=400
        )

    if not isinstance(data, dict):

        return JsonResponse(
            {
                "success": False,
                "error": "Invalid request data."
            },
            status=400
        )


    # -----------------------------------------------------
    # DESTINATION
    # -----------------------------------------------------

    destination = str(
        data.get(
            "destination",
            ""
        )
    ).strip()

    if not destination:

        return JsonResponse(
            {
                "success": False,
                "error": "Destination is required."
            },
            status=400
        )


    # -----------------------------------------------------
    # DAYS
    # -----------------------------------------------------

    days = safe_integer(
        data.get(
            "days",
            4
        ),
        default=4
    )

    days = max(
        1,
        min(days, 30)
    )


    # -----------------------------------------------------
    # TRAVELERS
    # -----------------------------------------------------

    travelers = safe_integer(
        data.get(
            "travelers",
            1
        ),
        default=1
    )

    travelers = max(
        1,
        min(travelers, 20)
    )


    # -----------------------------------------------------
    # BUDGET
    # -----------------------------------------------------

    budget = safe_integer(
        data.get(
            "budget",
            0
        )
    )


    # -----------------------------------------------------
    # OTHER DETAILS
    # -----------------------------------------------------

    origin = str(
        data.get(
            "origin",
            ""
        )
    ).strip()

    interests = str(
        data.get(
            "interests",
            ""
        )
    ).strip()

    hotel_style = str(
        data.get(
            "hotel_style",
            "Budget"
        )
    ).strip()

    notes = str(
        data.get(
            "notes",
            ""
        )
    ).strip()


    # -----------------------------------------------------
    # GENERATE AI PLAN
    # -----------------------------------------------------

    try:

        result = build_trip_plan(
            destination=destination,
            days=days,
            travelers=travelers,
            budget=budget,
            interests=interests,
            hotel_style=hotel_style,
        )

    except Exception as exc:

        print(
            "AI PLANNING ERROR:",
            exc
        )

        return JsonResponse(
            {
                "success": False,
                "error": (
                    "AI planning failed. "
                    f"{str(exc)}"
                ),
            },
            status=500
        )


    # -----------------------------------------------------
    # VALIDATE AI RESPONSE
    # -----------------------------------------------------

    if not isinstance(result, dict):

        return JsonResponse(
            {
                "success": False,
                "error": "AI returned an invalid response."
            },
            status=500
        )


    itinerary = result.get(
        "itinerary",
        []
    )

    if not isinstance(itinerary, list):

        return JsonResponse(
            {
                "success": False,
                "error": (
                    "AI returned an invalid "
                    "itinerary format."
                ),
            },
            status=500
        )


    # -----------------------------------------------------
    # CLEAN ITINERARY
    # -----------------------------------------------------

    itinerary_total = 0

    cleaned_itinerary = []

    for index, item in enumerate(
        itinerary,
        start=1
    ):

        if not isinstance(item, dict):
            continue

        estimated_cost = safe_integer(
            item.get(
                "estimated_cost",
                0
            )
        )

        itinerary_total += estimated_cost

        cleaned_itinerary.append(
            {
                "day_number": index,

                "title": str(
                    item.get(
                        "title",
                        f"Day {index}"
                    )
                ),

                "morning": str(
                    item.get(
                        "morning",
                        ""
                    )
                ),

                "afternoon": str(
                    item.get(
                        "afternoon",
                        ""
                    )
                ),

                "evening": str(
                    item.get(
                        "evening",
                        ""
                    )
                ),

                "estimated_cost":
                    estimated_cost,
            }
        )


    itinerary = cleaned_itinerary


    # -----------------------------------------------------
    # TOTAL COST
    # -----------------------------------------------------

    ai_total = safe_integer(
        result.get(
            "estimated_total_cost",
            0
        )
    )

    estimated_total_cost = ai_total

    if estimated_total_cost <= 0:
        estimated_total_cost = itinerary_total

    if (
        estimated_total_cost <= 0
        and budget > 0
    ):
        estimated_total_cost = budget


    # -----------------------------------------------------
    # BUDGET ANALYSIS
    # -----------------------------------------------------

    raw_budget_analysis = result.get(
        "budget_analysis",
        {}
    )

    if not isinstance(
        raw_budget_analysis,
        dict
    ):
        raw_budget_analysis = {}


    accommodation = safe_integer(
        raw_budget_analysis.get(
            "accommodation",
            0
        )
    )

    transportation = safe_integer(
        raw_budget_analysis.get(
            "transportation",
            0
        )
    )

    food = safe_integer(
        raw_budget_analysis.get(
            "food",
            0
        )
    )

    activities = safe_integer(
        raw_budget_analysis.get(
            "activities",
            0
        )
    )

    miscellaneous = safe_integer(
        raw_budget_analysis.get(
            "miscellaneous",
            0
        )
    )


    breakdown_total = (
        accommodation
        + transportation
        + food
        + activities
        + miscellaneous
    )


    if (
        breakdown_total <= 0
        and estimated_total_cost > 0
    ):

        budget_analysis = (
            create_budget_breakdown(
                estimated_total_cost
            )
        )

    else:

        budget_analysis = {
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


    # -----------------------------------------------------
    # TIPS
    # -----------------------------------------------------

    tips = result.get(
        "tips",
        []
    )

    if not isinstance(
        tips,
        list
    ):
        tips = []

    tips = [
        str(tip)
        for tip in tips
    ]


    # -----------------------------------------------------
    # PACKING LIST
    # -----------------------------------------------------

    packing_list = result.get(
        "packing_list",
        []
    )

    if not isinstance(
        packing_list,
        list
    ):
        packing_list = []

    packing_list = [
        str(item)
        for item in packing_list
    ]


    # -----------------------------------------------------
    # NORMALIZE RESPONSE
    # -----------------------------------------------------

    result["destination"] = destination
    result["days"] = days
    result["travelers"] = travelers
    result["budget"] = budget
    result["origin"] = origin
    result["interests"] = interests
    result["hotel_style"] = hotel_style
    result["notes"] = notes

    result["estimated_total_cost"] = (
        estimated_total_cost
    )

    result["currency"] = "INR"

    result["budget_analysis"] = (
        budget_analysis
    )

    result["itinerary"] = itinerary
    result["tips"] = tips
    result["packing_list"] = packing_list


    # -----------------------------------------------------
    # SAVE TO DATABASE
    # -----------------------------------------------------

    try:

        with transaction.atomic():

            trip = Trip.objects.create(

                title=(
                    f"{destination} "
                    "Smart Trip"
                ),

                destination=destination,
                origin=origin,
                days=days,
                travelers=travelers,
                budget=budget,
                interests=interests,
                hotel_style=hotel_style,
                notes=notes,
            )


            for index, item in enumerate(
                itinerary,
                start=1
            ):

                ItineraryDay.objects.create(

                    trip=trip,

                    day_number=index,

                    title=str(
                        item.get(
                            "title",
                            f"Day {index}"
                        )
                    ),

                    morning=str(
                        item.get(
                            "morning",
                            ""
                        )
                    ),

                    afternoon=str(
                        item.get(
                            "afternoon",
                            ""
                        )
                    ),

                    evening=str(
                        item.get(
                            "evening",
                            ""
                        )
                    ),

                    estimated_cost=safe_integer(
                        item.get(
                            "estimated_cost",
                            0
                        )
                    ),
                )


    except Exception as exc:

        print(
            "DATABASE SAVE ERROR:",
            exc
        )

        return JsonResponse(
            {
                "success": False,
                "error": (
                    "The AI plan was generated, "
                    "but it could not be saved: "
                    f"{str(exc)}"
                ),
            },
            status=500
        )


    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    result["success"] = True
    result["trip_id"] = trip.id

    return JsonResponse(
        result
    )


@staff_member_required(login_url="/admin-login/")
def admin_dashboard(request):

    trips = Trip.objects.all().order_by("-created_at")

    total_trips = trips.count()

    total_travelers = sum(
        trip.travelers or 0
        for trip in trips
    )

    total_budget = (
        trips.aggregate(
            total=Sum("budget")
        ).get("total") or 0
    )

    total_destinations = (
        trips.values("destination")
        .distinct()
        .count()
    )

    recent_trips = trips[:10]

    return render(
        request,
        "travel/admin_dashboard.html",
        {
            "total_trips": total_trips,
            "total_travelers": total_travelers,
            "total_budget": total_budget,
            "total_destinations": total_destinations,
            "recent_trips": recent_trips,
        }
    )

@staff_member_required(login_url="/admin-login/")
def admin_trip_detail(request, trip_id):

    trip = Trip.objects.get(
        id=trip_id
    )

    itinerary = ItineraryDay.objects.filter(
        trip=trip
    ).order_by("day_number")

    return render(
        request,
        "travel/admin_trip_detail.html",
        {
            "trip": trip,
            "itinerary": itinerary,
        }
    )
