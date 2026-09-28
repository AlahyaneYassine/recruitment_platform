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
    profession = forms.CharField(required=False)  # <-- Add this field

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
                education=self.cleaned_data['education'],
                profession=self.cleaned_data.get('profession', '') 
            )
        return user
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ce courriel est déjà utilisé.")
        return email

class RecruiterSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    company_name = forms.CharField(required=True)
    company_description = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(required=True)
    company_address = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_recruiter = True
        if commit:
            user.save()
            recruiter = Recruiter.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_description=self.cleaned_data['company_description'],
                phone_number=self.cleaned_data['phone_number'],
                company_address=self.cleaned_data['company_address']
            )
        return user

# Ces formulaires doivent être au niveau racine, pas dans RecruiterSignUpForm
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

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = ['company_name', 'company_description', 'phone_number', 'company_address', 'company_logo']
        widgets = {
            'company_description': forms.Textarea(attrs={'rows': 3}),
            'company_address': forms.Textarea(attrs={'rows': 3}),
        }

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')  # Supprime le champ password
##
from django.contrib.auth.forms import AuthenticationForm

class RecruiterLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email ou nom d\'utilisateur'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Mot de passe'
        })