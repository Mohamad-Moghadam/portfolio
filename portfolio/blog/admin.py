from django.contrib import admin
from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_editable = ('status',)
    list_per_page = 10
    list_max_show_all = 100
    list_display_links = ('title', 'author')
    list_select_related = ('author',)
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'content')