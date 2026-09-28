from django import forms
from .models import Application
from apps.messaging.models import Message

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'cover_letter', 'cv']
        widgets = {
            'cover_letter': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
                'placeholder': 'Téléchargez votre lettre de motivation...'
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            })
        }

    # Changer le label de 'cover_letter' pour "Lettre de motivation"
    cover_letter = forms.FileField(label="Lettre de motivation")
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']  # Use 'body' instead of 'content'
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Écrivez votre message ici...'
            })
        }

