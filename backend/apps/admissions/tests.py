from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from .models import AdmissionEnquiry


class AdmissionEnquiryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("admissions:index")

    def test_valid_ajax_enquiry_submission(self):
        mail.outbox.clear()
        payload = {
            "child_name": "Aarav Sharma",
            "age": 6,
            "needs": "Needs support with sensory integration and speech development.",
            "program_of_interest": "Inclusive Learning",
            "parent_name": "Mathan Sharma",
            "parent_email": "mathan@example.com",
            "parent_phone": "+919883805821",
            "preferred_contact": "whatsapp",
            "message": "Looking forward to hearing from you.",
            "consent_privacy": "on",
            "captcha_answer": 7,
            "website": "",
            "is_ajax": "1",
        }
        response = self.client.post(
            self.url,
            payload,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("safe", data["message"].lower())
        self.assertEqual(AdmissionEnquiry.objects.count(), 1)
        enquiry = AdmissionEnquiry.objects.first()
        self.assertEqual(enquiry.child_name, "Aarav Sharma")

        # Verify email alert dispatched to enquiry@sparshinclusiveeducation.com
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("enquiry@sparshinclusiveeducation.com", email.to)
        self.assertIn("[Sparsh Quick Enquiry]", email.subject)
        self.assertIn("Aarav Sharma", email.body)
        self.assertIn("Mathan Sharma", email.body)

    def test_invalid_ajax_enquiry_submission(self):
        payload = {
            "child_name": "",
            "age": "",
            "needs": "Short",
            "captcha_answer": 0,
            "is_ajax": "1",
        }
        response = self.client.post(
            self.url,
            payload,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("child_name", data["errors"])
        self.assertIn("captcha_answer", data["errors"])

    def test_enquiry_is_saved_when_notification_email_fails(self):
        payload = {
            "child_name": "Aarav Sharma",
            "age": 6,
            "needs": "Needs support with sensory integration and speech development.",
            "program_of_interest": "Inclusive Learning",
            "parent_name": "Mathan Sharma",
            "parent_email": "mathan@example.com",
            "parent_phone": "+919883805821",
            "preferred_contact": "whatsapp",
            "message": "Looking forward to hearing from you.",
            "consent_privacy": "on",
            "captcha_answer": 7,
            "website": "",
            "is_ajax": "1",
        }
        with patch("django.core.mail.send_mail", side_effect=OSError("connection refused")):
            with self.assertLogs("apps.core.mail", level="ERROR") as logs:
                response = self.client.post(
                    self.url,
                    payload,
                    HTTP_X_REQUESTED_WITH="XMLHttpRequest",
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(AdmissionEnquiry.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn("admissions notification email failed", "\n".join(logs.output))


class AdmissionEnquiryAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword123"
        )
        self.client.force_login(self.admin_user)
        self.enquiry = AdmissionEnquiry.objects.create(
            child_name="Rhea Verma",
            age=8,
            needs="Attention and reading support.",
            program_of_interest="Early Intervention",
            parent_name="Ananya Verma",
            parent_email="ananya@example.com",
            parent_phone="+919876543210",
            preferred_contact="whatsapp",
            message="Please share details.",
            consent_privacy=True,
        )

    def test_admin_download_csv_view(self):
        url = reverse("admin:admissions_admissionenquiry_download_csv")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("sparsh_admission_enquiries_report_", response["Content-Disposition"])
        content = response.content.decode("utf-8-sig")
        self.assertIn("Enquiry ID", content)
        self.assertIn("Child Name", content)
        self.assertIn("Rhea Verma", content)
        self.assertIn("Ananya Verma", content)
        self.assertIn("ananya@example.com", content)

    def test_admin_changelist_page_renders_download_button(self):
        url = reverse("admin:admissions_admissionenquiry_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Download Report (.CSV)")
        self.assertContains(response, "download-csv/")
