from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.jobs.models import Job
from .models import Application

User = get_user_model()

class ApplicationModelTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter',
            password='testpass123',
            is_recruiter=True
        )
        self.candidate = User.objects.create_user(
            username='candidate',
            password='testpass123',
            is_candidate=True
        )
        self.job = Job.objects.create(
            title='Développeur Python',
            recruiter=self.recruiter,
            description='Description du poste',
            requirements='Compétences requises'
        )

    def test_application_creation(self):
        application = Application.objects.create(
            candidate=self.candidate,
            job=self.job,
            cover_letter='Lettre de motivation',
            cv='cv.pdf'
        )
        self.assertEqual(application.status, 'PENDING')