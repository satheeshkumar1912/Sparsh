from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods

from apps.programs.models import Program, FeaturePillar
from apps.people.models import TeamMember
from apps.content.models import (
    Testimonial,
    SiteStat,
    GalleryItem,
    FAQ,
    ContactMessage,
)
from apps.admissions.forms import ContactForm, AdmissionEnquiryForm


def home(request):
    stats = SiteStat.get_solo()
    context = {
        "page_title": "Home",
        "meta_description": (
            "Sparsh Inclusive Education — neurodiverse-affirming learning where "
            "every child has a place and every child has potential."
        ),
        "pillars": FeaturePillar.objects.filter(is_published=True)[:6],
        "welcome_programs": Program.objects.filter(is_published=True, is_featured=True)[:4],
        "gallery": GalleryItem.objects.filter(is_published=True)[:6],
        "stats": stats,
        "testimonials": Testimonial.objects.filter(
            is_published=True, consent_given=True, is_featured=True
        )[:6],
        "faqs": FAQ.objects.filter(is_published=True)[:8],
        "admission_form": AdmissionEnquiryForm(),
        "programs": Program.objects.filter(is_published=True),
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(
        request,
        "core/about.html",
        {
            "page_title": "About Us",
            "meta_description": "Learn about Sparsh Inclusive Education — our mission, values, and commitment to every learner.",
            "team_preview": TeamMember.objects.filter(is_published=True)[:3],
        },
    )


def inclusive_education(request):
    return render(
        request,
        "core/inclusive_education.html",
        {
            "page_title": "Inclusive Education",
            "meta_description": "What inclusive education means at Sparsh — belonging, support, and limitless possibilities.",
            "pillars": FeaturePillar.objects.filter(is_published=True),
        },
    )


def approach(request):
    return render(
        request,
        "core/approach.html",
        {
            "page_title": "Our Approach",
            "meta_description": "Connection before curriculum — Sparsh's neurodiverse-affirming approach to learning and care.",
        },
    )


def parents_corner(request):
    return render(
        request,
        "core/parents_corner.html",
        {
            "page_title": "Parents’ Corner",
            "meta_description": "Resources, guidance, and community for families partnering with Sparsh.",
            "faqs": FAQ.objects.filter(is_published=True),
            "testimonials": Testimonial.objects.filter(
                is_published=True, consent_given=True
            )[:4],
        },
    )


@require_http_methods(["GET", "POST"])
def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ContactMessage.objects.create(
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            phone=form.cleaned_data.get("phone", ""),
            subject=form.cleaned_data["subject"],
            message=form.cleaned_data["message"],
        )
        recipient = getattr(settings, "CONTACT_EMAIL", "enquiry@sparshinclusiveeducation.com")
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@sparshinclusiveeducation.com")
        try:
            send_mail(
                subject=f"[Sparsh Contact] {form.cleaned_data['subject']}",
                message=(
                    f"New message received from Sparsh Website Contact Form:\n\n"
                    f"Name: {form.cleaned_data['name']}\n"
                    f"Email: {form.cleaned_data['email']}\n"
                    f"Phone: {form.cleaned_data.get('phone', 'N/A')}\n"
                    f"Subject: {form.cleaned_data['subject']}\n\n"
                    f"Message:\n{form.cleaned_data['message']}\n"
                ),
                from_email=from_email,
                recipient_list=[recipient],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(
            request,
            "Thank you — we’ve received your message and will reply soon.",
        )
        return redirect("core:contact")
    return render(
        request,
        "core/contact.html",
        {
            "page_title": "Contact",
            "meta_description": "Get in touch with Sparsh Inclusive Education.",
            "form": form,
        },
    )


def accessibility_statement(request):
    return render(
        request,
        "legal/accessibility.html",
        {"page_title": "Accessibility Statement"},
    )


def privacy_policy(request):
    return render(
        request,
        "legal/privacy.html",
        {"page_title": "Privacy Policy"},
    )


def terms(request):
    return render(
        request,
        "legal/terms.html",
        {"page_title": "Terms of Use"},
    )
