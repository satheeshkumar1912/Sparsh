from django.db import models
from django.utils.text import slugify


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    role = models.CharField(max_length=160)
    bio = models.TextField()
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    email = models.EmailField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Team member"
        verbose_name_plural = "Team members"

    def __str__(self):
        return f"{self.name} — {self.role}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        super().save(*args, **kwargs)


class Advisor(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    specialty = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to="advisors/", blank=True, null=True)
    affiliation = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} — {self.specialty}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        super().save(*args, **kwargs)
