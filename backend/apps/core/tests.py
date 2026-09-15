from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from apps.content.models import ContactMessage


class ContactViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("core:contact")

    def test_valid_contact_form_submission(self):
        mail.outbox.clear()
        payload = {
            "name": "Pooja Reddy",
            "email": "pooja@example.com",
            "phone": "+919876543211",
            "subject": "Inquiry about occupational therapy",
            "message": "We would like to understand your therapy programs.",
            "captcha_answer": 7,
            "website": "",
        }
        response = self.client.post(self.url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, "Pooja Reddy")
        self.assertEqual(msg.subject, "Inquiry about occupational therapy")

        # Verify email alert dispatched to enquiry@sparshinclusiveeducation.com
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("enquiry@sparshinclusiveeducation.com", email.to)
        self.assertIn("[Sparsh Contact]", email.subject)
        self.assertIn("Pooja Reddy", email.body)
        self.assertIn("pooja@example.com", email.body)

    def test_contact_form_mandatory_fields(self):
        # Empty payload - all fields should fail validation
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("name", form.errors)
        self.assertIn("email", form.errors)
        self.assertIn("phone", form.errors)
        self.assertIn("subject", form.errors)
        self.assertIn("message", form.errors)
        self.assertIn("captcha_answer", form.errors)


class ContactMessageAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword123"
        )
        self.client.force_login(self.admin_user)
        self.msg = ContactMessage.objects.create(
            name="Vikram Rao",
            email="vikram@example.com",
            phone="+919888877777",
            subject="Partnership inquiry",
            message="Interested in school collaboration.",
        )

    def test_admin_download_csv_view(self):
        url = reverse("admin:content_contactmessage_download_csv")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("sparsh_contact_messages_report_", response["Content-Disposition"])
        content = response.content.decode("utf-8-sig")
        self.assertIn("Message ID", content)
        self.assertIn("Sender Name", content)
        self.assertIn("Vikram Rao", content)
        self.assertIn("vikram@example.com", content)
        self.assertIn("Partnership inquiry", content)

    def test_admin_changelist_page_renders_download_button(self):
        url = reverse("admin:content_contactmessage_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Download Report (.CSV)")
        self.assertContains(response, "download-csv/")
