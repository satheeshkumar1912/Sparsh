from django.test import TestCase, Client
from django.urls import reverse
from .models import AdmissionEnquiry


class AdmissionEnquiryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("admissions:index")

    def test_valid_ajax_enquiry_submission(self):
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
