from django.shortcuts import render

from .models import TeamMember, Advisor


def team_list(request):
    return render(
        request,
        "people/team.html",
        {
            "page_title": "Our Team",
            "meta_description": "Meet the educators, therapists, and guides at Sparsh Inclusive Education.",
            "members": TeamMember.objects.filter(is_published=True),
        },
    )


def advisors_list(request):
    return render(
        request,
        "people/advisors.html",
        {
            "page_title": "Advisors",
            "meta_description": "Expert advisors supporting Sparsh’s inclusive education practice.",
            "advisors": Advisor.objects.filter(is_published=True),
        },
    )
