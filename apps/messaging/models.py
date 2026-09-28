from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Message(models.Model):
    application = models.ForeignKey(
        'applications.Application',  # Référence l'applications.Application
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='messages',
        verbose_name="Related Application"
    )
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return self.subject or f"Message #{self.pk}"

    def mark_as_read(self):
        if not self.read_at:
            self.read_at = timezone.now()
            self.save()