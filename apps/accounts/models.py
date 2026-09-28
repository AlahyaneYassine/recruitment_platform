from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

def save(self, *args, **kwargs):
        if self.is_candidate and self.is_recruiter:
            raise ValueError("Un utilisateur ne peut pas être à la fois recruteur et candidat.")
        super().save(*args, **kwargs)


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    skills = models.TextField()
    experience = models.TextField()
    education = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Champ ajouté
    profession = models.CharField(max_length=100, blank=True, null=True) 
    def __str__(self):
        return f"Candidat: {self.user.username}"
    # Ajoutez d'autres champs spécifiques aux candidats

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    phone_number = models.CharField(max_length=20)
    company_address = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)  # Champ ajouté
    def __str__(self):
        return f"Recruteur: {self.company_name} ({self.user.username})"
    # Ajoutez d'autres champs spécifiques aux recruteurs
    