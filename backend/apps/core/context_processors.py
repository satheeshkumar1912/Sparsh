from django.conf import settings
from django.urls import reverse


ASSESSMENT_DROPDOWN = [
    {
        "label": "Need-Based Assessment",
        "anchor": "need-based-assessment",
    },
    {
        "label": "Examination Accommodations",
        "anchor": "examination-accommodations",
    },
    {
        "label": "NIOS Support",
        "anchor": "nios-support",
    },
    {
        "label": "Scribe Support",
        "anchor": "scribe-support",
    },
    {
        "label": "Examination Readiness",
        "anchor": "examination-readiness",
    },
    {
        "label": "Assistive Learning and Access Support",
        "anchor": "assistive-learning-and-access-support",
    },
]

ADMISSIONS_DROPDOWN = [
    {
        "label": "Who We Support",
        "anchor": "who-we-support",
    },
    {
        "label": "Admission Process",
        "anchor": "admission-process",
    },
    {
        "label": "Initial Consultation",
        "anchor": "initial-consultation",
    },
    {
        "label": "Screening , Assessment & Programme support",
        "anchor": "iep-framework",
    },
    {
        "label": "Enquire and apply",
        "anchor": "enquiry-section",
    },
]


def _nav_dropdown_links(url_name, items, link_labels=None):
    base = reverse(url_name)
    links = []
    for item in items:
        entry = {"label": item["label"]}
        if link_labels is None or item["label"] in link_labels:
            entry["url"] = f"{base}#{item['anchor']}"
        links.append(entry)
    return links


def site_settings(request):
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_URL": settings.SITE_URL,
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
        "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
        "NAV_ITEMS": [
            {"label": "Home", "url_name": "core:home"},
            {"label": "About Us", "url_name": "core:about"},
            {"label": "Inclusive Education", "url_name": "core:inclusive_education"},
            {"label": "Programs", "url_name": "programs:list"},
            {
                "label": "Assessment",
                "url_name": "core:assessment",
                "dropdown": _nav_dropdown_links("core:assessment", ASSESSMENT_DROPDOWN),
            },
            {
                "label": "Admissions",
                "url_name": "admissions:index",
                "dropdown": _nav_dropdown_links(
                    "admissions:index",
                    ADMISSIONS_DROPDOWN,
                    link_labels={"Enquire and apply"},
                ),
            },
            {"label": "Partner With Us", "url_name": "core:partner"},
            {"label": "Contact Us", "url_name": "core:contact"},
        ],
    }
