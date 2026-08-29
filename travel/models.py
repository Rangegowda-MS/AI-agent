from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=120, unique=True)
    country = models.CharField(max_length=80, default="India")
    category = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    starting_price = models.PositiveIntegerField(default=0)
    best_time = models.CharField(max_length=120, blank=True)
    image_url = models.URLField(blank=True)
    def __str__(self): return self.name

class Trip(models.Model):
    title = models.CharField(max_length=180)
    destination = models.CharField(max_length=120)
    origin = models.CharField(max_length=120, blank=True)
    days = models.PositiveIntegerField(default=3)
    travelers = models.PositiveIntegerField(default=1)
    budget = models.PositiveIntegerField(default=0)
    interests = models.TextField(blank=True)
    hotel_style = models.CharField(max_length=80, default="Budget")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title

class ItineraryDay(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="itinerary_days")
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=180)
    morning = models.TextField(blank=True)
    afternoon = models.TextField(blank=True)
    evening = models.TextField(blank=True)
    estimated_cost = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["day_number"]
    def __str__(self): return f"{self.trip.title} - Day {self.day_number}"
