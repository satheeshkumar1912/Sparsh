from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class AdmissionEnquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        SCHEDULED = "scheduled", "Visit Scheduled"
        ENROLLED = "enrolled", "Enrolled"
        CLOSED = "closed", "Closed"

    child_name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(25)]
    )
    needs = models.TextField(
        help_text="Describe learning needs, strengths, or support areas"
    )
    program_of_interest = models.CharField(max_length=200, blank=True)
    parent_name = models.CharField(max_length=120)
    parent_email = models.EmailField()
    parent_phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^[\d\s\+\-\(\)]{7,20}$",
                message="Enter a valid phone number.",
            )
        ],
    )
    preferred_contact = models.CharField(
        max_length=20,
        choices=[
            ("phone", "Phone"),
            ("email", "Email"),
            ("whatsapp", "WhatsApp"),
        ],
        default="whatsapp",
    )
    message = models.TextField(blank=True)
    consent_privacy = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Internal staff notes")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Admission enquiry"
        verbose_name_plural = "Admission enquiries"

    def __str__(self):
        return f"{self.child_name} ({self.parent_name}) — {self.status}"

    @property
    def parent_contact(self):
        return f"{self.parent_email} | {self.parent_phone}"
