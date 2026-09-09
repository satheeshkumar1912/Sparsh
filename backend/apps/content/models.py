from django.db import models


class Testimonial(models.Model):
    parent_name = models.CharField(max_length=120)
    quote = models.TextField()
    program = models.CharField(max_length=160, blank=True)
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    role_label = models.CharField(
        max_length=80, default="Parent", help_text="e.g. Parent, Educator"
    )
    is_featured = models.BooleanField(default=True)
    consent_given = models.BooleanField(
        default=True, help_text="Photo/quote used with consent"
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.parent_name}: {self.quote[:50]}…"


class SiteStat(models.Model):
    """Singleton-style impact statistics."""

    learners_supported = models.PositiveIntegerField(default=0)
    partner_schools = models.PositiveIntegerField(default=0)
    educators_trained = models.PositiveIntegerField(default=0)
    families_recommend = models.PositiveIntegerField(
        default=0, help_text="Percentage of families who recommend us"
    )
    learners_qualifier = models.CharField(max_length=80, default="since 2015")
    schools_qualifier = models.CharField(max_length=80, default="across regions")
    educators_qualifier = models.CharField(max_length=80, default="workshops & coaching")
    recommend_qualifier = models.CharField(max_length=80, default="of surveyed families")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site statistics"
        verbose_name_plural = "Site statistics"

    def __str__(self):
        return "Impact statistics"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class GalleryItem(models.Model):
    title = models.CharField(max_length=160)
    caption = models.CharField(max_length=200)
    quote = models.CharField(max_length=280, blank=True)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    image_alt = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Gallery item"
        verbose_name_plural = "Gallery items"

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=80, default="General")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "question"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.subject}"
