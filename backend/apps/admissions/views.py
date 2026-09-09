from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods

from apps.content.models import FAQ
from apps.programs.models import Program
from .forms import AdmissionEnquiryForm


ADMISSIONS_TIMELINE = [
    {
        "step": 1,
        "title": "Gentle enquiry",
        "text": "Share a little about your child — no pressure, no jargon. We’ll listen first.",
    },
    {
        "step": 2,
        "title": "Conversation",
        "text": "A warm call or WhatsApp chat with our admissions guide to understand hopes and needs.",
    },
    {
        "step": 3,
        "title": "Visit & observation",
        "text": "Optional campus visit so your child can explore spaces at their own pace.",
    },
    {
        "step": 4,
        "title": "Collaborative plan",
        "text": "Together we map a thoughtful placement and support plan.",
    },
    {
        "step": 5,
        "title": "Welcome",
        "text": "Onboarding with family partnership — settling in with care and clarity.",
    },
]


@require_http_methods(["GET", "POST"])
def admissions_index(request):
    form = AdmissionEnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        enquiry = form.save(commit=False)
        enquiry.ip_address = _client_ip(request)
        enquiry.user_agent = request.META.get("HTTP_USER_AGENT", "")[:300]
        enquiry.save()
        try:
            send_mail(
                subject=f"[Sparsh Admissions] Enquiry for {enquiry.child_name}",
                message=(
                    f"Child: {enquiry.child_name}, age {enquiry.age}\n"
                    f"Needs: {enquiry.needs}\n"
                    f"Program: {enquiry.program_of_interest}\n"
                    f"Parent: {enquiry.parent_name}\n"
                    f"Contact: {enquiry.parent_email} / {enquiry.parent_phone}\n"
                    f"Preferred: {enquiry.preferred_contact}\n"
                    f"Message: {enquiry.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMISSIONS_NOTIFY_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(
            request,
            "Thank you. Your enquiry is safe with us — a Sparsh team member will reach out soon.",
        )
        return redirect("admissions:thanks")

    admission_faqs = list(
        FAQ.objects.filter(is_published=True, category__icontains="Admission")[:5]
    )
    if not admission_faqs:
        admission_faqs = list(FAQ.objects.filter(is_published=True)[:5])

    return render(
        request,
        "admissions/index.html",
        {
            "page_title": "Admissions",
            "meta_description": "Begin your child's journey with Sparsh — a gentle, supportive admissions process.",
            "form": form,
            "timeline": ADMISSIONS_TIMELINE,
            "faqs": admission_faqs,
            "programs": Program.objects.filter(is_published=True),
            "whatsapp_url": f"https://wa.me/{settings.WHATSAPP_NUMBER}?text=Hello%20Sparsh%2C%20I%27d%20like%20to%20enquire%20about%20admissions.",
        },
    )


def admissions_thanks(request):
    return render(
        request,
        "admissions/thanks.html",
        {
            "page_title": "Enquiry received",
            "meta_description": "Thank you for your Sparsh admissions enquiry.",
        },
    )


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
