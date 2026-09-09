from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Program(models.Model):
    class Category(models.TextChoices):
        EARLY_INTERVENTION = "early_intervention", "Early Intervention"
        INCLUSIVE_LEARNING = "inclusive_learning", "Inclusive Learning"
        THERAPY_SUPPORT = "therapy_support", "Therapy & Family Support"
        ACADEMIC_PATHWAYS = "academic_pathways", "Academic Pathways"
        EDUCATOR_TRAINING = "educator_training", "Educator Training"
        OTHER = "other", "Other"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    age_group = models.CharField(max_length=100, help_text="e.g. Ages 3–8")
    category = models.CharField(
        max_length=40, choices=Category.choices, default=Category.OTHER
    )
    icon = models.CharField(
        max_length=40,
        blank=True,
        help_text="CSS icon key, e.g. butterfly, heart, book",
    )
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    highlights = models.TextField(
        blank=True, help_text="One highlight per line"
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:200]
            slug = base
            n = 1
            while Program.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("programs:detail", kwargs={"slug": self.slug})

    @property
    def highlight_list(self):
        return [h.strip() for h in self.highlights.splitlines() if h.strip()]


class FeaturePillar(models.Model):
    """Clickable feature pillars on the homepage."""

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(max_length=280)
    body = models.TextField()
    icon = models.CharField(max_length=40, default="leaf")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Feature pillar"
        verbose_name_plural = "Feature pillars"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("programs:pillar_detail", kwargs={"slug": self.slug})
