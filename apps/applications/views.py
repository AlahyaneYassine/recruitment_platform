from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from .models import Application
from .forms import ApplicationForm
from apps.jobs.models import Job
from apps.messaging.models import Message
from .forms import MessageForm

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    if not request.user.is_candidate:
        messages.error(request, "Seuls les candidats peuvent postuler.")
        return redirect('jobs:job_detail', slug=job.slug)

    already_applied = Application.objects.filter(candidate=request.user, job=job).exists()
    if already_applied:
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect('jobs:job_detail', slug=job.slug)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = request.user
            application.job = job
            application.save()
            messages.success(request, "Votre candidature a été envoyée avec succès!")
            return redirect('applications:application_detail', pk=application.pk)
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply_form.html', {
        'form': form,
        'job': job,
        'already_applied': already_applied
    })
from django.http import JsonResponse

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.user != application.candidate and request.user != application.job.recruiter:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Gestion AJAX pour les messages
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'body' in request.POST:  # Si c'est un envoi de message
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.recipient = application.candidate
                message.application = application
                message.save()
                return JsonResponse({'success': True})
            return JsonResponse({'error': 'Invalid form data'}, status=400)
        
        elif 'status' in request.POST:  # Si c'est une mise à jour de statut
            new_status = request.POST.get('status')
            if new_status in dict(Application.STATUS_CHOICES).keys():
                application.status = new_status
                application.save()
                return JsonResponse({
                    'success': True,
                    'new_status': new_status,
                    'status_display': application.get_status_display()
                })
            return JsonResponse({'error': 'Invalid status'}, status=400)

    # Gestion normale pour les requêtes non-AJAX
    message_form = MessageForm(initial={
        'subject': f"À propos de votre candidature pour {application.job.title}"
    }) if request.user == application.job.recruiter else None

    return render(request, 'applications/application_detail.html', {
        'application': application,
        'message_form': message_form,
        'status_choices': Application.STATUS_CHOICES
    })

@login_required
def application_list(request):
    if request.user.is_candidate:
        applications = Application.objects.filter(candidate=request.user)
    elif request.user.is_recruiter:
        applications = Application.objects.filter(job__recruiter=request.user)
    else:
        messages.error(request, "Accès non autorisé.")
        return redirect('home')

    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'applications/application_list.html', {
        'applications': applications,
        'status_filter': status_filter
    })

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
@login_required
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.user != application.job.recruiter:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    new_status = request.POST.get('status')
    if new_status not in dict(Application.STATUS_CHOICES):
        return JsonResponse({'error': 'Invalid status'}, status=400)

    application.status = new_status
    application.save()
    
    return JsonResponse({
        'success': True,
        'new_status': new_status,
        'status_display': application.get_status_display(),
        'badge_class': get_badge_class(new_status)
    })

def get_badge_class(status):
    badge_classes = {
        'ACCEPTED': 'bg-success',
        'REJECTED': 'bg-danger',
        'INTERVIEW': 'bg-info',
        'REVIEWED': 'bg-warning text-dark',
        'PENDING': 'bg-secondary'
    }
    return badge_classes.get(status, 'bg-secondary')

@login_required
def job_list_to_apply(request):
    if not request.user.is_candidate:
        messages.error(request, "Seuls les candidats peuvent voir cette page.")
        return redirect('home')

    jobs = Job.objects.filter(is_active=True)
    return render(request, 'applications/job_list_to_apply.html', {'jobs': jobs})

@login_required
def available_jobs(request):
    if not request.user.is_candidate:
        messages.error(request, "Seuls les candidats peuvent voir cette page.")
        return redirect('home')

    applied_job_ids = Application.objects.filter(
        candidate=request.user
    ).values_list('job_id', flat=True)

    jobs = Job.objects.filter(
        is_active=True
    ).exclude(
        id__in=applied_job_ids
    ).order_by('-created_at')

    return render(request, 'applications/available_jobs.html', {'jobs': jobs})

@login_required
def application_list_for_job(request, job_id):
    if not request.user.is_recruiter:
        messages.error(request, "Accès réservé aux recruteurs.")
        return redirect('home')

    job = get_object_or_404(Job, pk=job_id, recruiter=request.user)
    applications = Application.objects.filter(job=job)

    # Ajoutez cette partie pour gérer la mise à jour du statut
    if request.method == 'POST' and 'status' in request.POST:
        application_id = request.POST.get('application_id')
        application = get_object_or_404(Application, pk=application_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Application.STATUS_CHOICES).keys():
            application.status = new_status
            application.save()
            messages.success(request, f"Statut de {application.candidate.get_full_name()} mis à jour!")
            return redirect('applications:application_list_for_job', job_id=job_id)

    return render(request, 'applications/applications_for_job.html', {
        'job': job,
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES
    })

@login_required
def conversation(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    if request.user not in [application.candidate, application.job.recruiter]:
        messages.error(request, "Accès non autorisé.")
        return redirect('home')

    message_list = Message.objects.filter(
        application=application
    ).order_by('timestamp')

    if request.user == application.candidate:
        unread_messages = message_list.filter(is_read=False)
        for msg in unread_messages:
            msg.mark_as_read()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.application = application
            message.sender = request.user
            message.recipient = (
                application.candidate if request.user == application.job.recruiter
                else application.job.recruiter
            )
            message.save()
            return redirect('messaging:conversation', application_id=application.id)
    else:
        form = MessageForm()

    return render(request, 'messaging/conversation.html', {
        'application': application,
        'message_list': message_list,
        'form': form
    })
