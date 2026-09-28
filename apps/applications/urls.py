from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Candidatures
    path('postuler/<int:job_id>/', views.apply_job, name='apply_job'),
    path('mes-candidatures/', views.application_list, name='application_list'),
    path('candidature/<int:pk>/', views.application_detail, name='application_detail'),

    # Gestion des statuts
    path('candidature/<int:pk>/modifier-statut/', views.update_application_status, name='update_status'),

    # Offres d'emploi
    path('offres-disponibles/', views.available_jobs, name='available_jobs'),
    path('offres/<int:job_id>/candidatures/', views.application_list_for_job, name='application_list_for_job'),

    # Messagerie
    path('candidature/<int:application_id>/conversation/', views.conversation, name='conversation'),
]
