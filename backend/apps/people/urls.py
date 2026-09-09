from django.urls import path
from . import views

app_name = "people"

urlpatterns = [
    path("team/", views.team_list, name="team"),
    path("advisors/", views.advisors_list, name="advisors"),
]
