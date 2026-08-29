from django import forms
class TripPlannerForm(forms.Form):
    destination = forms.CharField(max_length=120)
    origin = forms.CharField(max_length=120, required=False)
    days = forms.IntegerField(min_value=1, max_value=30, initial=4)
    travelers = forms.IntegerField(min_value=1, max_value=20, initial=2)
    budget = forms.IntegerField(min_value=0, initial=20000)
    interests = forms.CharField(required=False)
    hotel_style = forms.ChoiceField(choices=[("Budget","Budget"),("Comfort","Comfort"),("Luxury","Luxury")])
    notes = forms.CharField(required=False)
