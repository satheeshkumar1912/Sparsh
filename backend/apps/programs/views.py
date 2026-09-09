from django.shortcuts import render, get_object_or_404

from .models import Program, FeaturePillar


def program_list(request):
    programs = Program.objects.filter(is_published=True)
    category = request.GET.get("category")
    if category:
        programs = programs.filter(category=category)
    return render(
        request,
        "programs/list.html",
        {
            "page_title": "Programs",
            "meta_description": "Explore Sparsh programs — early intervention, inclusive learning, therapy support, and academic pathways.",
            "programs": programs,
            "categories": Program.Category.choices,
            "active_category": category or "",
        },
    )


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug, is_published=True)
    related = (
        Program.objects.filter(is_published=True, category=program.category)
        .exclude(pk=program.pk)[:3]
    )
    return render(
        request,
        "programs/detail.html",
        {
            "page_title": program.name,
            "meta_description": program.short_description or program.description[:160],
            "program": program,
            "related": related,
        },
    )


def pillar_detail(request, slug):
    pillar = get_object_or_404(FeaturePillar, slug=slug, is_published=True)
    others = FeaturePillar.objects.filter(is_published=True).exclude(pk=pillar.pk)[:5]
    return render(
        request,
        "programs/pillar_detail.html",
        {
            "page_title": pillar.title,
            "meta_description": pillar.summary,
            "pillar": pillar,
            "others": others,
        },
    )
