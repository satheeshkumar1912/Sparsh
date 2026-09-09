from django.urls import path
from . import views

app_name = "admissions"

urlpatterns = [
    path("", views.admissions_index, name="index"),
    path("thank-you/", views.admissions_thanks, name="thanks"),
]
