from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('candidate__username', 'job__title')
    readonly_fields = ('applied_date', 'updated_date')