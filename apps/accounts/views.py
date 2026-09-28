from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import (
    CandidateProfileForm, 
    RecruiterProfileForm, 
    CandidateSignUpForm, 
    RecruiterSignUpForm, 
    UserEditForm,
    RecruiterLoginForm
)
from django.contrib.auth.forms import AuthenticationForm
from apps.jobs.models import Job
from apps.applications.models import Application
from .models import Recruiter  # Ajout de l'import manquant

# Inscription Candidat
def candidate_signup(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue sur votre espace candidat.')
            return redirect('accounts:candidate_profile')
    else:
        form = CandidateSignUpForm()
    return render(request, 'accounts/signup/candidate_signup.html', {
        'form': form,
        'user_type': 'candidate'
    })

# Inscription Recruteur
def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription recruteur réussie ! Configurez votre profil maintenant.')
            return redirect('accounts:recruiter_profile')
    else:
        form = RecruiterSignUpForm()
    return render(request, 'accounts/signup/recruiter_signup.html', {
        'form': form,
        'user_type': 'recruiter'
    })

# Connexion Candidat
class CandidateLoginView(LoginView):
    template_name = 'accounts/login/candidate_login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm
    
    def get_success_url(self):
        if hasattr(self.request.user, 'candidate'):
            return reverse_lazy('accounts:candidate_profile')
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, "Email ou mot de passe incorrect. Veuillez réessayer.")
        return super().form_invalid(form)

# Connexion Recruteur
class RecruiterLoginView(LoginView):
    template_name = 'accounts/login/recruiter_login.html'
    form_class = RecruiterLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if hasattr(self.request.user, 'recruiter'):
            return reverse_lazy('accounts:recruiter_profile')
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, "Identifiants invalides pour un compte recruteur.")
        return super().form_invalid(form)

# Profil Candidat
@login_required
def candidate_profile(request):
    if not hasattr(request.user, 'candidate'):
        return redirect('accounts:candidate_signup')
    
    candidate = request.user.candidate
    applications = Application.objects.filter(candidate=request.user).select_related('job')
    
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=candidate)
        user_form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('accounts:candidate_profile')
    else:
        form = CandidateProfileForm(instance=candidate)
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/profile/candidate_profile.html', {
        'form': form,
        'user_form': user_form,
        'applications': applications,
        'active_tab': 'profile'
    })

# Profil Recruteur
@login_required
def recruiter_profile(request):
    if not hasattr(request.user, 'recruiter'):
        return redirect('accounts:recruiter_signup')
    
    recruiter = request.user.recruiter
    jobs = Job.objects.filter(recruiter=request.user).annotate(
        application_count=Count('applications')
    ).order_by('-created_at')[:5]

    if request.method == 'POST':
        form = RecruiterProfileForm(request.POST, request.FILES, instance=recruiter)
        user_form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Profil recruteur mis à jour avec succès !')
            return redirect('accounts:recruiter_profile')
    else:
        form = RecruiterProfileForm(instance=recruiter)
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/profile/recruiter_profile.html', {
        'form': form,
        'user_form': user_form,
        'jobs': jobs,
        'active_tab': 'profile'
    })

# Déconnexion
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')

# Page d'accueil améliorée
def home_view(request):
    # Construire le queryset de base
    recent_jobs = Job.objects.filter(is_active=True).annotate(
        application_count=Count('applications')
    ).order_by('-created_at')
    
    # Filtrer les jobs déjà postulés pour les candidats
    if request.user.is_authenticated and hasattr(request.user, 'is_candidate') and request.user.is_candidate:
        applied_job_ids = Application.objects.filter(
            candidate=request.user
        ).values_list('job_id', flat=True)
        recent_jobs = recent_jobs.exclude(id__in=applied_job_ids)
    
    # Prendre seulement 6 jobs
    recent_jobs = recent_jobs[:6]
    
    # Préparer les statistiques
    stats = {
        'total_jobs': Job.objects.filter(is_active=True).count(),
        'total_companies': Recruiter.objects.values('company_name').distinct().count(),
    }
    
    return render(request, 'home/home.html', {
        'recent_jobs': recent_jobs,
        'user': request.user,
        'stats': stats,
        'active_page': 'home'
    })

# Vue personnalisée pour la réinitialisation du mot de passe
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset/password_reset_form.html'
    email_template_name = 'accounts/password_reset/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')