from django.conf import settings


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
            {"label": "Our Approach", "url_name": "core:approach"},
            {"label": "Our Team", "url_name": "people:team"},
            {"label": "Advisors", "url_name": "people:advisors"},
            {"label": "Parents’ Corner", "url_name": "core:parents_corner"},
            {"label": "Admissions", "url_name": "admissions:index"},
            {"label": "Contact", "url_name": "core:contact"},
        ],
    }
