from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from apps.messaging.models import Message
from apps.applications.models import Application
from .forms import MessageForm

@login_required
def inbox(request):
    message_list = request.user.received_messages.all().order_by('-sent_at')
    return render(request, 'messaging/inbox.html', {'message_list': message_list})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    
    if message.recipient == request.user:
        message.mark_as_read()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = message.sender if request.user == message.recipient else message.recipient
            reply.parent_message = message
            reply.application = message.application
            reply.save()
            django_messages.success(request, 'Votre réponse a été envoyée avec succès.')
            return redirect('messaging:inbox')
    else:
        form = MessageForm(initial={
            'subject': f"Re: {message.subject}",
            'body': f"\n\n--- Message original ---\n{message.body}"
        })
    
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'form': form
    })

@login_required
def send_message(request, recipient_id=None, application_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if recipient_id:
                message.recipient_id = recipient_id
            if application_id:
                message.application_id = application_id
            message.save()
            django_messages.success(request, 'Votre message a été envoyé avec succès.')
            return redirect('messaging:inbox')
    else:
        initial = {}
        if recipient_id:
            initial['recipient'] = recipient_id
        form = MessageForm(initial=initial)
    
    return render(request, 'messaging/send_message.html', {'form': form})

@login_required
def reply_to_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    
    # Vérification stricte des permissions
    if not request.user.is_recruiter or request.user != application.job.recruiter:
        raise PermissionDenied("Seuls les recruteurs responsables peuvent répondre")

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = application.candidate
            message.application = application
            message.subject = f"Re: Candidature pour {application.job.title}"
            message.save()
            
            # Mettre à jour le statut si nécessaire
            if 'status' in request.POST:
                application.status = request.POST['status']
                application.save()
            
            django_messages.success(request, 'Votre réponse a été envoyée au candidat.')
            return redirect('applications:application_detail', pk=application.id)
    else:
        form = MessageForm(initial={
            'subject': f"Candidature pour {application.job.title}",
            'body': f"Bonjour {application.candidate.first_name},\n\n"
        })

    return render(request, 'messaging/reply_to_application.html', {
        'form': form,
        'application': application,
        'status_choices': Application.STATUS_CHOICES
    })
@login_required
def empty_inbox(request):
    if request.method == 'POST':
        # Récupère tous les messages non lus de l'utilisateur
        messages_to_delete = Message.objects.filter(recipient=request.user)
        count = messages_to_delete.count()
        
        # Suppression en masse
        messages_to_delete.delete()
        
        # Message de confirmation
        django_messages.success(request, f'{count} message(s) ont été supprimés de votre boîte de réception.')
        
        return redirect('messaging:inbox')
    
    raise PermissionDenied("Méthode non autorisée")

@login_required
def inbox(request):
    message_list = request.user.received_messages.all().order_by('-sent_at')
    unread_count = request.user.received_messages.filter(read_at__isnull=True).count()
    
    return render(request, 'messaging/inbox.html', {
        'message_list': message_list,
        'unread_count': unread_count
    })

@login_required
def candidate_inbox(request):
    if not request.user.is_candidate:
        raise PermissionDenied("Accès réservé aux candidats")
    
    messages = Message.objects.filter(
        recipient=request.user
    ).select_related(
        'sender__recruiter',
        'application__job'
    ).order_by('-sent_at')
    
    unread_count = messages.filter(read_at__isnull=True).count()
    
    return render(request, 'messaging/candidate_inbox.html', {
        'messages': messages,
        'unread_count': unread_count
    })