# api/admin.py
from django.contrib import admin
from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ('id', 'model_used', 'status', 'timestamp', 'processing_time', 'prompt_preview')

    # Make 'id' and 'model_used' clickable
    list_display_links = ('id', 'model_used')

    # Enable filtering by specific fields
    list_filter = ('model_used', 'status', 'timestamp', 'processing_time')

    # Add date hierarchy for easier navigation
    date_hierarchy = 'timestamp'

    # Enable search for specific fields
    search_fields = ('prompt', 'response_text', 'model_used', 'status')

    # Default sorting by 'timestamp'
    ordering = ('-timestamp',)

    # Make 'status' editable in the list view
    list_editable = ('status',)

    # Mark 'timestamp' and 'processing_time' as read-only
    readonly_fields = ('timestamp', 'processing_time')

    # Display preview of the prompt
    def prompt_preview(self, obj):
        return obj.prompt[:50] + "..." if len(obj.prompt) > 50 else obj.prompt
    prompt_preview.short_description = 'Prompt Preview'

    # Set number of items per page
    list_per_page = 25

    # Custom actions
    actions = ['mark_completed', 'delete_selected']

    # Mark selected responses as 'completed'
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = 'Mark selected responses as completed'
