from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Candidate, Recruiter
from .forms import CandidateSignUpForm, RecruiterSignUpForm

class CandidateInline(admin.StackedInline):
    model = Candidate
    extra = 0
    can_delete = False
    verbose_name_plural = 'Détails Candidat'

class RecruiterInline(admin.StackedInline):
    model = Recruiter
    extra = 0
    can_delete = False
    verbose_name_plural = 'Détails Recruteur'

class CustomUserAdmin(UserAdmin):
    inlines = (CandidateInline, RecruiterInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_candidate', 'is_recruiter')
    list_filter = ('is_candidate', 'is_recruiter')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    # Pour séparer création et modification dans l'admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Désenregistrer puis réenregistrer le modèle User
admin.site.register(User, CustomUserAdmin)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'skills_short')
    search_fields = ('user__username', 'user__email', 'skills')
    
    def skills_short(self, obj):
        return obj.skills[:50] + '...' if len(obj.skills) > 50 else obj.skills
    skills_short.short_description = 'Compétences'

@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'phone_number')
    search_fields = ('user__username', 'company_name', 'user__email')