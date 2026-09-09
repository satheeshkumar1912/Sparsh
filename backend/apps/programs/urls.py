from django.urls import path
from . import views

app_name = "programs"

urlpatterns = [
    path("", views.program_list, name="list"),
    path("pillars/<slug:slug>/", views.pillar_detail, name="pillar_detail"),
    path("<slug:slug>/", views.program_detail, name="detail"),
]
