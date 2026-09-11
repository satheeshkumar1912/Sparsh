from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import AdmissionEnquiry


class AdmissionEnquiryForm(forms.ModelForm):
    """Secure admissions enquiry form with honeypot CAPTCHA."""

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
                "class": "hp-field",
            }
        ),
        label="",
    )
    captcha_answer = forms.IntegerField(
        label="Security check: What is 3 + 4?",
        min_value=0,
        max_value=20,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter number (e.g. 7)",
                "inputmode": "numeric",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = AdmissionEnquiry
        fields = [
            "child_name",
            "age",
            "needs",
            "program_of_interest",
            "parent_name",
            "parent_email",
            "parent_phone",
            "preferred_contact",
            "message",
            "consent_privacy",
        ]
        widgets = {
            "child_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Aarav Sharma"}
            ),
            "age": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 25,
                    "placeholder": "e.g. 6",
                }
            ),
            "needs": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Briefly describe your child's strengths, interests, or support needs...",
                }
            ),
            "program_of_interest": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select or type program (e.g. Inclusive Learning)",
                    "list": "program-suggestions",
                }
            ),
            "parent_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your full name"}
            ),
            "parent_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "parent@example.com"}
            ),
            "parent_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+91 98765 43210",
                    "autocomplete": "tel",
                }
            ),
            "preferred_contact": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Any specific questions, preferred timings, or remarks? (Optional)",
                }
            ),
            "consent_privacy": forms.CheckboxInput(attrs={"class": "form-check"}),
        }
        labels = {
            "child_name": "Child's name",
            "age": "Child's age",
            "needs": "Learning needs & strengths",
            "program_of_interest": "Program of interest",
            "parent_name": "Parent / guardian name",
            "parent_email": "Email",
            "parent_phone": "Phone / WhatsApp",
            "preferred_contact": "Preferred contact method",
            "message": "Additional message",
            "consent_privacy": "I agree to the Privacy Policy and consent to Sparsh contacting me about this enquiry.",
        }

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise ValidationError("Spam detected.")
        return value

    def clean_captcha_answer(self):
        answer = self.cleaned_data.get("captcha_answer")
        if answer != 7:
            raise ValidationError("Please solve the security check correctly.")
        return answer

    def clean_consent_privacy(self):
        if not self.cleaned_data.get("consent_privacy"):
            raise ValidationError("Please accept the privacy policy to continue.")
        return self.cleaned_data["consent_privacy"]

    def clean_needs(self):
        needs = (self.cleaned_data.get("needs") or "").strip()
        if len(needs) < 10:
            raise ValidationError("Please share a little more detail (at least 10 characters).")
        return needs


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "you@example.com"}
        )
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone (optional)"}),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 5, "placeholder": "How can we help?"}
        )
    )
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
                "class": "hp-field",
            }
        ),
    )
    captcha_answer = forms.IntegerField(
        label="Security check: What is 2 + 5?",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "inputmode": "numeric", "autocomplete": "off"}
        ),
    )

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise ValidationError("Spam detected.")
        return ""

    def clean_captcha_answer(self):
        if self.cleaned_data.get("captcha_answer") != 7:
            raise ValidationError("Please solve the security check correctly.")
        return self.cleaned_data["captcha_answer"]
