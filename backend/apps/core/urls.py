from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("inclusive-education/", views.inclusive_education, name="inclusive_education"),
    path("our-approach/", views.approach, name="approach"),
    path("parents-corner/", views.parents_corner, name="parents_corner"),
    path("contact/", views.contact, name="contact"),
    path("accessibility/", views.accessibility_statement, name="accessibility"),
    path("privacy/", views.privacy_policy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
