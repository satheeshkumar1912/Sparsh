from django.shortcuts import render, get_object_or_404

from .models import Program, FeaturePillar


PROGRAM_PAGE_SECTIONS = [
    {
        "title": "Therapeutic Intervention & Family Support",
        "body": (
            "Our multidisciplinary team delivers personalised interventions that strengthen "
            "communication, participation, emotional well-being and everyday functioning. "
            "Families remain central to the journey through coordinated guidance, counselling "
            "and regular progress reviews."
        ),
        "points": [
            "Speech and Language Therapy",
            "Occupational Therapy",
            "Behavioural Intervention",
            "Psychological Counselling and Support",
            "Sensory Regulation Support",
            "Classroom Intervention",
            "Shadow-Teacher Placement and Support",
            "Parent Counselling and Family Guidance",
            "Individualised Planning and Periodic Reviews",
            "Integrated Learning and development approach .",
        ],
    },
    {
        "title": "Academic Pathways",
        "body": (
            "Flexible academic pathways support learners across mainstream, differentiated, "
            "functional and alternative curricula. Individualised planning, remedial education "
            "and appropriate assistive resources make learning accessible and future-focused."
        ),
        "points": [],
    },
    {
        "title": "Educator Training & Certification",
        "body": (
            "Sparsh equips educators and inclusion practitioners with practical capabilities "
            "for diverse classrooms. Training integrates inclusive practice, differentiated "
            "instruction, safeguarding, assistive technology and multidisciplinary collaboration."
        ),
        "note": (
            "Certificates of completion may be offered for Sparsh modules; regulated "
            "qualifications are represented only where formal approval or accreditation applies."
        ),
        "points": [],
    },
    {
        "title": "Vocational Training & Life Skills",
        "body": (
            "Strengths-led programmes prepare learners for independent living, purposeful "
            "engagement and future employment. Experiences may include practical skill "
            "development, workplace readiness, supported exposure and transition planning."
        ),
        "points": [],
    },
    {
        "title": "Sports & Endurance Training",
        "body": (
            "Adaptive sports and movement programmes strengthen fitness, coordination, "
            "endurance and confidence. Participation also nurtures perseverance, teamwork "
            "and emotional well-being."
        ),
        "points": [],
    },
    {
        "title": "Evening Therapies & Remedial Support",
        "body": (
            "Flexible after-school sessions provide personalised academic, developmental "
            "and therapeutic support. Individual and small-group formats enable focused "
            "intervention beyond regular school hours."
        ),
        "points": [],
    },
    {
        "title": "Weekend Cognitive Skill Development",
        "body": (
            "Engaging weekend experiences develop attention, memory, reasoning, "
            "communication and executive functioning. Play, projects and real-world "
            "challenges encourage creativity, collaboration and independent thinking."
        ),
        "points": [],
    },
]


def program_list(request):
    return render(
        request,
        "programs/list.html",
        {
            "page_title": "Programs",
            "meta_description": (
                "One ecosystem. Infinite possibilities — Sparsh programmes spanning therapy, "
                "academic pathways, educator training, vocational skills, sports and more."
            ),
            "program_sections": PROGRAM_PAGE_SECTIONS,
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
