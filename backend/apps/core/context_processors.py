from django.conf import settings


ASSESSMENT_DROPDOWN = [
    "Need-Based Assessment",
    "Examination Accommodations",
    "NIOS Support",
    "Scribe Support",
    "Examination Readiness",
    "Assistive Learning and Access Support",
]

ADMISSIONS_DROPDOWN = [
    "Who We Support",
    "Admission Process",
    "Initial Consultation",
    "Screening , Assessment & Programme support",
    "Enquire and apply",
]


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
                "dropdown": ASSESSMENT_DROPDOWN,
            },
            {
                "label": "Admissions",
                "dropdown": ADMISSIONS_DROPDOWN,
            },
            {"label": "Partner With Us", "url_name": "core:partner"},
            {"label": "Contact Us", "url_name": "core:contact"},
        ],
    }
