from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.text import slugify
from django.http import Http404
from .models import Job
from .forms import JobCreateForm, JobUpdateForm
from apps.accounts.models import Recruiter
from apps.applications.models import Application
import uuid

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True).order_by('-created_at')
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'is_candidate') and self.request.user.is_candidate:
            applied_jobs = Application.objects.filter(
                candidate=self.request.user
            ).values_list('job_id', flat=True)
            queryset = queryset.exclude(id__in=applied_jobs)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'is_candidate'):
            context['applied_job_ids'] = Application.objects.filter(
                candidate=self.request.user
            ).values_list('job_id', flat=True)
        return context

@login_required
def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    
    already_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'is_candidate') and request.user.is_candidate:
        already_applied = Application.objects.filter(
            candidate=request.user,
            job=job
        ).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied
    })

@login_required
def job_create(request):
    if not hasattr(request.user, 'recruiter'):
        messages.error(request, "Seuls les recruteurs peuvent créer des offres d'emploi.")
        return redirect('home')

    if request.method == 'POST':
        form = JobCreateForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            
            slug = slugify(job.title)
            if Job.objects.filter(slug=slug).exists():
                slug = f"{slug}-{uuid.uuid4().hex[:8]}"
            job.slug = slug
            
            job.save()
            messages.success(request, "L'offre d'emploi a été créée avec succès.")
            return redirect('jobs:job_manage')
    else:
        form = JobCreateForm()

    return render(request, 'jobs/job_create.html', {'form': form})

@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    if request.user != job.recruiter:
        messages.error(request, "Vous n'avez pas la permission de modifier cette offre.")
        return redirect('home')
    
    if request.method == 'POST':
        form = JobUpdateForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            
            if 'title' in form.changed_data:
                slug = slugify(job.title)
                if Job.objects.filter(slug=slug).exclude(pk=job.pk).exists():
                    slug = f"{slug}-{uuid.uuid4().hex[:8]}"
                job.slug = slug
            
            job.save()
            messages.success(request, "L'offre a été mise à jour avec succès.")
            return redirect('jobs:job_manage')
    else:
        form = JobUpdateForm(instance=job)
    
    return render(request, 'jobs/job_update.html', {'form': form, 'job': job})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    if request.user != job.recruiter:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette offre.")
        return redirect('home')
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, "L'offre a été supprimée avec succès.")
        return redirect('jobs:job_manage')
    
    return render(request, 'jobs/job_delete.html', {'job': job})

@login_required
def job_manage(request):
    if not hasattr(request.user, 'recruiter'):
        messages.error(request, "Seuls les recruteurs peuvent gérer les offres.")
        return redirect('home')

    # Récupération des paramètres de filtrage
    status_filter = request.GET.get('status')
    job_type_filter = request.GET.get('job_type')
    location_filter = request.GET.get('location')

    # Base queryset
    jobs = Job.objects.filter(recruiter=request.user).order_by('-created_at')

    # Application des filtres
    if status_filter == 'active':
        jobs = jobs.filter(is_active=True)
    elif status_filter == 'inactive':
        jobs = jobs.filter(is_active=False)

    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)

    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    # Préparation des données statistiques
    for job in jobs:
        job.pending_count = job.applications.filter(status='PENDING').count()
        job.reviewed_count = job.applications.filter(status='REVIEWED').count()
        job.interview_count = job.applications.filter(status='INTERVIEW').count()
        job.accepted_count = job.applications.filter(status='ACCEPTED').count()
        job.rejected_count = job.applications.filter(status='REJECTED').count()

    context = {
        'jobs': jobs,
        'app_counts': {job.id: job.applications.count() for job in jobs},
        'JOB_TYPES': Job.JOB_TYPES,
        'current_filters': {
            'status': status_filter,
            'job_type': job_type_filter,
            'location': location_filter,
        }
    }

    return render(request, 'jobs/job_manage.html', context)

def job_redirect(request, pk):
    try:
        job = Job.objects.get(pk=pk)
        if request.user.is_authenticated and hasattr(request.user, 'is_candidate') and request.user.is_candidate:
            if Application.objects.filter(candidate=request.user, job=job).exists():
                messages.info(request, "Vous avez déjà postulé à cette offre")
        return redirect('jobs:job_detail', slug=job.slug, permanent=True)
    except Job.DoesNotExist:
        raise Http404("Job does not exist")