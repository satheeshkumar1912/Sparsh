from django.core.management.base import BaseCommand

from apps.programs.models import Program, FeaturePillar
from apps.people.models import TeamMember, Advisor
from apps.content.models import Testimonial, SiteStat, GalleryItem, FAQ


class Command(BaseCommand):
    help = "Seed demo content for Sparsh Inclusive Education public site"

    def handle(self, *args, **options):
        self._stats()
        self._pillars()
        self._programs()
        self._team()
        self._advisors()
        self._testimonials()
        self._gallery()
        self._faqs()
        self.stdout.write(self.style.SUCCESS("Seed data loaded."))

    def _stats(self):
        SiteStat.objects.update_or_create(
            pk=1,
            defaults={
                "learners_supported": 2400,
                "partner_schools": 48,
                "educators_trained": 860,
                "families_recommend": 96,
                "learners_qualifier": "since 2015",
                "schools_qualifier": "across regions",
                "educators_qualifier": "workshops & coaching",
                "recommend_qualifier": "of surveyed families",
            },
        )

    def _pillars(self):
        pillars = [
            (
                "Neurodiverse-Affirming",
                "We honour how each brain learns — strengths first, stigma never.",
                "At Sparsh, neurodiversity is not a deficit to fix; it is a lens for designing richer classrooms. "
                "We adapt environments, pacing, and communication so learners can show what they know without masking who they are.",
                "brain",
                1,
            ),
            (
                "Mainstream Inclusion",
                "Belonging in shared spaces, with the right scaffolds around each child.",
                "Inclusion means meaningful participation — not proximity alone. We partner with mainstream schools "
                "to co-create access plans, peer belonging, and educator confidence.",
                "people",
                2,
            ),
            (
                "Early Intervention",
                "The earlier we connect, the wider the path ahead.",
                "Our early years work blends play, communication, sensory regulation, and family coaching — "
                "gentle, evidence-informed support when it matters most.",
                "sprout",
                3,
            ),
            (
                "Educator Training",
                "Classrooms change when teachers feel equipped and supported.",
                "From workshops to on-site coaching, we help educators build practical inclusive strategies "
                "that work on Monday morning — not just in theory.",
                "book",
                4,
            ),
            (
                "Family Partnerships",
                "Parents are co-experts. We walk beside you.",
                "Every plan is co-authored with families. We share language, celebrate progress, "
                "and hold space for the hard days with honesty and care.",
                "heart",
                5,
            ),
            (
                "Every Ability Welcome",
                "Different abilities. Limitless possibilities.",
                "Whether your child is navigating autism, ADHD, learning differences, developmental delays, "
                "or gifts that need stretching — Sparsh is a place of welcome.",
                "butterfly",
                6,
            ),
        ]
        for title, summary, body, icon, order in pillars:
            FeaturePillar.objects.update_or_create(
                slug=title.lower().replace(" ", "-").replace("’", ""),
                defaults={
                    "title": title,
                    "summary": summary,
                    "body": body,
                    "icon": icon,
                    "order": order,
                    "is_published": True,
                },
            )

    def _programs(self):
        programs = [
            {
                "name": "Early Intervention",
                "short_description": "Play-based support for young learners building foundations.",
                "description": (
                    "A nurturing programme for early years that weaves communication, sensory regulation, "
                    "motor play, and social connection. Families receive coaching so strategies travel home."
                ),
                "age_group": "Ages 2–6",
                "category": Program.Category.EARLY_INTERVENTION,
                "icon": "sprout",
                "highlights": "Play-based sessions\nParent coaching\nIndividual goals\nSensory-aware spaces",
                "is_featured": True,
                "order": 1,
            },
            {
                "name": "Inclusive Learning",
                "short_description": "Classroom experiences designed for belonging and growth.",
                "description": (
                    "Small-group and supported learning that builds literacy, numeracy, and life skills "
                    "while protecting joy. We design for attention, regulation, and peer connection."
                ),
                "age_group": "Ages 6–14",
                "category": Program.Category.INCLUSIVE_LEARNING,
                "icon": "book",
                "highlights": "Differentiated curriculum\nPeer belonging\nVisual supports\nStrengths profiling",
                "is_featured": True,
                "order": 2,
            },
            {
                "name": "Therapy & Family Support",
                "short_description": "Integrated therapies with families at the centre.",
                "description": (
                    "Speech, occupational, and behavioural supports coordinated with educators — "
                    "so children experience one coherent plan, not fragmented appointments."
                ),
                "age_group": "All ages",
                "category": Program.Category.THERAPY_SUPPORT,
                "icon": "heart",
                "highlights": "Multidisciplinary team\nFamily sessions\nSchool liaison\nProgress reviews",
                "is_featured": True,
                "order": 3,
            },
            {
                "name": "Academic Pathways",
                "short_description": "Flexible routes toward meaningful academic milestones.",
                "description": (
                    "From bridge programmes to mainstream readiness, we map academic pathways "
                    "that respect pace, interests, and long-term wellbeing."
                ),
                "age_group": "Ages 8–18",
                "category": Program.Category.ACADEMIC_PATHWAYS,
                "icon": "path",
                "highlights": "Individual learning plans\nExam accommodations support\nCareer exploration\nTransition planning",
                "is_featured": True,
                "order": 4,
            },
            {
                "name": "Educator Training & Coaching",
                "short_description": "Practical inclusive practice for schools and teachers.",
                "description": (
                    "Workshops, PLCs, and classroom coaching that turn inclusive intent into daily habits — "
                    "for partner schools and independent educators."
                ),
                "age_group": "Educators & schools",
                "category": Program.Category.EDUCATOR_TRAINING,
                "icon": "people",
                "highlights": "On-site coaching\nUDL strategies\nBehaviour as communication\nLeadership consults",
                "is_featured": False,
                "order": 5,
            },
        ]
        for p in programs:
            Program.objects.update_or_create(name=p["name"], defaults={**p, "is_published": True})

    def _team(self):
        members = [
            (
                "Ananya Mehta",
                "Director of Inclusive Practice",
                "Ananya has spent 15 years building classrooms where neurodiverse learners lead with their strengths. "
                "She believes connection is the first curriculum.",
            ),
            (
                "Rahul Desai",
                "Lead Educator — Early Years",
                "Rahul designs play spaces that invite curiosity without overwhelm. "
                "Parents know him for gentle humour and crystal-clear progress notes.",
            ),
            (
                "Dr. Priya Nair",
                "Clinical Lead — Therapies",
                "Priya integrates speech and OT goals into everyday learning moments, "
                "so therapy feels like living — not another appointment.",
            ),
            (
                "Sofia Khan",
                "Family Partnerships Lead",
                "Sofia walks families through admissions and beyond, translating systems into human language "
                "and making sure no parent feels alone.",
            ),
        ]
        for i, (name, role, bio) in enumerate(members, start=1):
            TeamMember.objects.update_or_create(
                name=name,
                defaults={"role": role, "bio": bio, "order": i, "is_published": True},
            )

    def _advisors(self):
        advisors = [
            (
                "Prof. Leela Krishnan",
                "Inclusive Pedagogy",
                "Advisor on curriculum design for mixed-ability classrooms.",
                "National Institute of Education Studies",
            ),
            (
                "Dr. Marcus Okonkwo",
                "Developmental Paediatrics",
                "Guides early identification pathways and family-centred care models.",
                "Children’s Developmental Network",
            ),
            (
                "Aisha Rahman",
                "Neurodiversity Advocacy",
                "Lived-experience advisor ensuring Sparsh policies remain affirming and practical.",
                "Neurodiversity Collective",
            ),
        ]
        for i, (name, specialty, bio, affiliation) in enumerate(advisors, start=1):
            Advisor.objects.update_or_create(
                name=name,
                defaults={
                    "specialty": specialty,
                    "bio": bio,
                    "affiliation": affiliation,
                    "order": i,
                    "is_published": True,
                },
            )

    def _testimonials(self):
        items = [
            (
                "Meera S.",
                "For the first time, school doesn’t feel like a battle. Sparsh saw my son’s humour before his challenges.",
                "Inclusive Learning",
            ),
            (
                "Arjun & Neha P.",
                "The admissions conversation was gentle. No checklist of deficits — just curiosity about who our daughter is.",
                "Early Intervention",
            ),
            (
                "Kavitha R.",
                "Teacher training with Sparsh changed our whole wing. Inclusion stopped being a poster and became practice.",
                "Educator Training",
            ),
            (
                "David L.",
                "Therapy goals finally match classroom goals. We’re one team now — and our child can feel it.",
                "Therapy & Family Support",
            ),
        ]
        for i, (name, quote, program) in enumerate(items, start=1):
            Testimonial.objects.update_or_create(
                parent_name=name,
                defaults={
                    "quote": quote,
                    "program": program,
                    "role_label": "Parent" if "Educator" not in program else "Partner Educator",
                    "consent_given": True,
                    "is_featured": True,
                    "is_published": True,
                    "order": i,
                },
            )

    def _gallery(self):
        items = [
            (
                "Morning circle",
                "Classroom experiences",
                "Every voice has a turn — spoken, signed, or shown.",
                "Children gathered in a calm classroom morning circle",
            ),
            (
                "Colour & rhythm",
                "Art & music",
                "Creativity is a language every child already speaks.",
                "Learners painting and exploring musical instruments",
            ),
            (
                "Friendship outdoors",
                "Play & friendship",
                "Belonging grows in shared laughter and patient play.",
                "Children playing together outdoors in a green courtyard",
            ),
            (
                "Quiet corners",
                "Classroom experiences",
                "Regulation spaces are part of learning, not a timeout.",
                "A soft sensory corner with cushions and soft light",
            ),
            (
                "Studio hour",
                "Art & music",
                "Hands busy, minds open — joy is a serious outcome.",
                "Art studio with children’s collaborative mural",
            ),
            (
                "Peer partners",
                "Play & friendship",
                "Inclusion is practiced in the small moments between friends.",
                "Two children collaborating on a building activity",
            ),
        ]
        for i, (title, caption, quote, alt) in enumerate(items, start=1):
            GalleryItem.objects.update_or_create(
                title=title,
                defaults={
                    "caption": caption,
                    "quote": quote,
                    "image_alt": alt,
                    "order": i,
                    "is_published": True,
                },
            )

    def _faqs(self):
        faqs = [
            (
                "Who is Sparsh for?",
                "Sparsh welcomes learners with diverse abilities — including autism, ADHD, learning differences, "
                "developmental delays, and children who thrive with thoughtful, affirming support. "
                "We also partner with schools and educators.",
                "General",
            ),
            (
                "How does the admissions process work?",
                "Start with a gentle enquiry form or WhatsApp message. We’ll schedule a conversation, "
                "optionally arrange a visit, and co-create a placement plan — never rushed, never clinical cold.",
                "Admissions",
            ),
            (
                "Do you only serve neurodivergent children?",
                "Our practice is neurodiverse-affirming and inclusive. Many learners join through partner schools "
                "where mixed classrooms benefit from Sparsh scaffolds and training.",
                "General",
            ),
            (
                "Can parents stay involved?",
                "Absolutely. Family partnership is a pillar of our work — coaching, progress reviews, "
                "and shared language between home and Sparsh.",
                "Parents",
            ),
            (
                "What ages do you support?",
                "Programmes span early intervention (from about age 2) through adolescent academic pathways. "
                "Share your child’s age in the enquiry and we’ll guide next steps.",
                "Admissions",
            ),
            (
                "Is Sparsh a replacement for mainstream school?",
                "Sometimes Sparsh is a primary learning home; sometimes we bridge toward or support within "
                "mainstream settings. The right path is decided together.",
                "Programs",
            ),
            (
                "How do you measure progress?",
                "Through goals that matter to the child and family — communication, regulation, belonging, "
                "and academic growth — reviewed in plain language, not opaque scores alone.",
                "Programs",
            ),
            (
                "How can schools partner with Sparsh?",
                "We offer educator training, classroom coaching, and inclusion consults. "
                "Use the Contact page or Admissions enquiry and select Educator Training.",
                "General",
            ),
        ]
        for i, (q, a, cat) in enumerate(faqs, start=1):
            FAQ.objects.update_or_create(
                question=q,
                defaults={"answer": a, "category": cat, "order": i, "is_published": True},
            )
