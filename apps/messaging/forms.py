from django import forms
from apps.messaging.models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']  # Version finale avec seulement ces champs
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Écrivez votre message ici...'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet du message'
            })
        }

    def __init__(self, *args, **kwargs):
        # Pour le cas où on aurait besoin du champ recipient
        self.recipient = kwargs.pop('recipient', None)
        super().__init__(*args, **kwargs)
        
        # Si on veut ajouter dynamiquement le champ recipient
        if hasattr(self, 'add_recipient_field') and self.add_recipient_field:
            self.fields['recipient'] = forms.ModelChoiceField(
                queryset=User.objects.exclude(id=self.initial.get('sender_id', 0)),
                widget=forms.Select(attrs={'class': 'form-control'})
            )