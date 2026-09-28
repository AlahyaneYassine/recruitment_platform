from django.urls import path
from . import views
from .views import job_redirect

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('manage/', views.job_manage, name='job_manage'),
    path('id/<int:pk>/', views.job_redirect, name='job_redirect'),
    path('<int:pk>/update/', views.job_update, name='job_update'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('<slug:slug>/', views.job_detail, name='job_detail'),  # mettre en dernier !
]
