from django.urls import path
from django.urls import path, reverse_lazy  # Ajoutez reverse_lazy ici
from django.contrib.auth import views as auth_views
from .views import (
    candidate_signup,
    recruiter_signup,
    CandidateLoginView,
    RecruiterLoginView, 
    candidate_profile,
    recruiter_profile,  # Ajoutez cette importation
    logout_view,
    home_view
)


app_name = 'accounts'


urlpatterns = [
    # Authentification
    path('candidate/signup/', candidate_signup, name='candidate_signup'),
    path('recruiter/signup/', recruiter_signup, name='recruiter_signup'),
    path('login/candidate/', CandidateLoginView.as_view(), name='candidate_login'),
    path('login/recruiter/', RecruiterLoginView.as_view(), name='recruiter_login'),  # Ajoutez cette ligne
    path('logout/', logout_view, name='logout'),
    
    # Profil
    path('profile/candidate/', candidate_profile, name='candidate_profile'),
    path('profile/recruiter/', recruiter_profile, name='recruiter_profile'),
    
    # Réinitialisation mot de passe
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset/password_reset_form.html',
             subject_template_name='accounts/password_reset/password_reset_subject.txt',
             email_template_name='accounts/password_reset/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done')
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
        
    
    # Home
    path('', home_view, name='home'),

    
]