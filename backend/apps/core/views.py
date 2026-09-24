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


SPARSH_PATHWAY = [
    {
        "letter": "S",
        "title": "Strengths-Led Assessment",
        "text": "Understanding every learner beyond the diagnosis.",
    },
    {
        "letter": "P",
        "title": "Personalised Planning",
        "text": "Designing an individual pathway for meaningful progress.",
    },
    {
        "letter": "A",
        "title": "Academic & Therapeutic Advancement",
        "text": "Integrating remedial learning with need-based interventions.",
    },
    {
        "letter": "R",
        "title": "Responsive Partnerships",
        "text": "Connecting schools, educators, therapists, and families.",
    },
    {
        "letter": "S",
        "title": "Skills for Life and Work",
        "text": "Building confidence through life and vocational skills.",
    },
    {
        "letter": "H",
        "title": "Holistic Growth & Independence",
        "text": "Enabling every learner to participate, belong, and thrive.",
    },
]


INCLUSIVE_OFFERINGS = [
    {
        "title": "School Readiness",
        "body": (
            "Thoughtfully designed programmes prepare learners for classroom routines, "
            "communication, participation and social engagement. Each pathway builds the "
            "confidence and foundational skills required for a positive transition into school."
        ),
    },
    {
        "title": "Classroom Inclusion Support",
        "body": (
            "Sparsh provides coordinated classroom and shadow-teacher support that helps "
            "learners access, engage and belong. We collaborate with educators and families "
            "to ensure consistency across school and home."
        ),
    },
    {
        "title": "Curriculum-Integrated Special Education",
        "body": (
            "Individualised special education is thoughtfully aligned with the learner’s "
            "academic and functional goals. Appropriate accommodations, differentiated "
            "instruction and Individualised Education Plans make learning accessible and meaningful."
        ),
    },
    {
        "title": "Transition Programmes",
        "body": (
            "Structured transition support prepares learners for movement across grades, "
            "schools, curricula and important life stages. Each transition is planned around "
            "readiness, continuity and growing independence."
        ),
    },
    {
        "title": "School Inclusion Solutions",
        "body": (
            "We partner with schools to strengthen inclusive practices, educator capability "
            "and learner-support systems. Every engagement is shaped around the institution’s "
            "context, priorities and long-term vision."
        ),
    },
]


def inclusive_education(request):
    return render(
        request,
        "core/inclusive_education.html",
        {
            "page_title": "Inclusive Education",
            "meta_description": (
                "SPARSH creates a continuous pathway from understanding the learner "
                "to building meaningful independence."
            ),
            "sparsh_pathway": SPARSH_PATHWAY,
            "inclusive_offerings": INCLUSIVE_OFFERINGS,
        },
    )


ASSESSMENT_SERVICES = [
    {
        "slug": "need-based-assessment",
        "title": "Need-Based Assessment",
        "text": (
            "A clear picture of strengths, support needs, and practical next steps. "
            "Recommendations are personalised, evidence-informed and developed with "
            "appropriately qualified professionals."
        ),
    },
    {
        "slug": "examination-accommodations",
        "title": "Examination Accommodations",
        "text": (
            "Navigate exam access arrangements with clarity and the right documentation — "
            "within applicable school and board rules and timelines."
        ),
    },
    {
        "slug": "nios-support",
        "title": "NIOS Support",
        "text": (
            "Sparsh supports families exploring flexible academic pathways through the "
            "National Institute of Open Schooling. Guidance may include subject planning, "
            "academic preparation, registration support and examination readiness, subject "
            "to applicable NIOS regulations."
        ),
    },
    {
        "slug": "scribe-support",
        "title": "Scribe Support",
        "text": (
            "Thoughtful scribe arrangements so learners can show what they know — with "
            "eligibility guidance, practice, and calm exam-day preparation."
        ),
    },
    {
        "slug": "examination-readiness",
        "title": "Examination Readiness",
        "text": (
            "Build calm, confident exam habits — content, pacing, sensory regulation, "
            "and exam-day plans practised together with families."
        ),
    },
    {
        "slug": "assistive-learning-and-access-support",
        "title": "Assistive Learning and Access Support",
        "text": (
            "Tools, strategies, and access supports that open learning — chosen for "
            "usefulness in real classrooms and at home."
        ),
    },
]


def assessment(request):
    return render(
        request,
        "core/assessment.html",
        {
            "page_title": "Assessment",
            "meta_description": (
                "Clarity for confident next steps — need-based assessment and "
                "academic-access guidance from Sparsh."
            ),
            "services": ASSESSMENT_SERVICES,
            "whatsapp_url": (
                f"https://wa.me/{settings.WHATSAPP_NUMBER}"
                "?text=Hello%20Sparsh%2C%20I%27d%20like%20to%20enquire%20about%20assessment."
            ),
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


PARTNERSHIP_CATEGORIES = [
    {
        "title": "Schools & Educational Institutions",
        "text": "Co-create inclusive classrooms, educator capacity, and learner pathways that make belonging practical every day.",
    },
    {
        "title": "Therapists & Professionals",
        "text": "Collaborate across disciplines so therapy goals, classroom supports, and family plans stay coherent and humane.",
    },
    {
        "title": "NGOs & Community Organisations",
        "text": "Join forces to expand community access, awareness, and sustainable inclusion beyond a single campus.",
    },
    {
        "title": "Corporate & CSR Partners",
        "text": "Invest in ethical, measurable inclusion initiatives that strengthen capability and opportunity for diverse learners.",
    },
    {
        "title": "Training & Knowledge Partners",
        "text": "Share expertise through workshops, research, and knowledge exchange that raise the standard of inclusive practice.",
    },
]


def partner(request):
    return render(
        request,
        "core/partner.html",
        {
            "page_title": "Partner With Us",
            "meta_description": (
                "Build inclusive futures with Sparsh — partnerships for schools, professionals, "
                "NGOs, CSR, and training organisations."
            ),
            "categories": PARTNERSHIP_CATEGORIES,
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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
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
    else:
        form = ContactForm()
    return render(
        request,
        "core/contact.html",
        {
            "page_title": "Contact Us",
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
