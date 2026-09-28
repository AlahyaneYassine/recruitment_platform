from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_company_name', 'location', 'job_type', 'is_active')
    list_filter = ('job_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'recruiter__username', 'recruiter__recruiter__company_name')
    prepopulated_fields = {'slug': ('title',)}
    
    def get_company_name(self, obj):
        if hasattr(obj.recruiter, 'recruiter'):
            return obj.recruiter.recruiter.company_name
        return "N/A"
    get_company_name.short_description = 'Company'