from django.db import models
from django.conf import settings
from apps.jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('REVIEWED', 'Examinée'),
        ('INTERVIEW', 'Entretien'),
        ('ACCEPTED', 'Acceptée'),
        ('REJECTED', 'Rejetée'),
    ]

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'is_candidate': True}
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    # Ajouter une valeur par défaut pour les champs non-nullables
    first_name = models.CharField(max_length=100, default='Nom')
    last_name = models.CharField(max_length=100, default='Prénom')
    email = models.EmailField(default='default@email.com')  # Valeur par défaut ici
    phone_number = models.CharField(max_length=15, default='0000000000')  # Exemple d'un numéro par défaut
    
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)
    cv = models.FileField(upload_to='cvs/')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('candidate', 'job')
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"