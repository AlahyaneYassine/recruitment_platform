from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()

class Job(models.Model):
    JOB_TYPES = [
        ('FULL', 'Full-time'),
        ('PART', 'Part-time'),
        ('CONT', 'Contract'),
        ('INTE', 'Internship'),
        ('TEMP', 'Temporary'),
    ]

    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_recruiter': True}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=4, choices=JOB_TYPES, default='FULL')
    salary = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_deadline = models.DateField(null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    def __str__(self):
        if hasattr(self.recruiter, 'recruiter') and self.recruiter.recruiter.company_name:
            return f"{self.title} - {self.recruiter.recruiter.company_name}"
        return f"{self.title} - {self.recruiter.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            if Job.objects.filter(slug=slug).exists():
                slug = f"{slug}-{uuid.uuid4().hex[:8]}"
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Jobs"