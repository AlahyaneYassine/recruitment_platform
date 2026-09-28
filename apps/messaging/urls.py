from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/empty/', views.empty_inbox, name='empty_inbox'),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('send/', views.send_message, name='send_message'),
    path('send/<int:recipient_id>/', views.send_message, name='send_to'),
    path('send/<int:recipient_id>/application/<int:application_id>/', 
         views.send_message, name='send_about_application'),
    path('application/<int:application_id>/reply/', 
         views.reply_to_application, name='reply_to_application'),
    path('candidate/inbox/', views.candidate_inbox, name='candidate_inbox'),
]