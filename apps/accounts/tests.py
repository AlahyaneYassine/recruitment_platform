from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Candidate, Recruiter

class CandidateSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    skills = forms.CharField(widget=forms.Textarea)
    experience = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_candidate = True
        if commit:
            user.save()
            candidate = Candidate.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                skills=self.cleaned_data['skills'],
                experience=self.cleaned_data['experience'],
                education=self.cleaned_data['education']
            )
        return user

# Formulaire de réinitialisation de mot de passe
class PasswordResetForm(forms.Form):
    email = forms.EmailField()

# Formulaire pour éditer les informations du profil
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['phone_number', 'address', 'skills', 'experience', 'education','profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 3}),
        }

# Formulaire pour la modification des informations utilisateur (nom, email, etc.)
class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')  # Supprime le champ password
