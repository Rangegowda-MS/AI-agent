from django.urls import path
from .views import generate_plan
urlpatterns = [path("plan/", generate_plan, name="generate_plan")]
