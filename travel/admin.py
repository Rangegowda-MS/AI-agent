from django.contrib import admin

from .models import Trip, ItineraryDay


# =========================================================
# ITINERARY DAY INLINE
# =========================================================

class ItineraryDayInline(admin.TabularInline):
    model = ItineraryDay
    extra = 0

    fields = (
        "day_number",
        "title",
        "morning",
        "afternoon",
        "evening",
        "estimated_cost",
    )

    ordering = (
        "day_number",
    )


# =========================================================
# TRIP ADMIN
# =========================================================

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "destination",
        "origin",
        "days",
        "travelers",
        "budget",
        "hotel_style",
        "created_at",
    )

    list_display_links = (
        "id",
        "destination",
    )

    list_filter = (
        "hotel_style",
        "days",
        "travelers",
        "created_at",
    )

    search_fields = (
        "destination",
        "origin",
        "interests",
        "notes",
        "title",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = [
        ItineraryDayInline,
    ]

    fieldsets = (
        (
            "Trip Information",
            {
                "fields": (
                    "title",
                    "destination",
                    "origin",
                    "days",
                    "travelers",
                )
            },
        ),
        (
            "Budget & Preferences",
            {
                "fields": (
                    "budget",
                    "hotel_style",
                    "interests",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "notes",
                    "created_at",
                )
            },
        ),
    )


# =========================================================
# ITINERARY DAY ADMIN
# =========================================================

@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "trip",
        "day_number",
        "title",
        "estimated_cost",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "day_number",
    )

    search_fields = (
        "title",
        "morning",
        "afternoon",
        "evening",
        "trip__destination",
    )

    ordering = (
        "trip",
        "day_number",
    )