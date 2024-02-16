from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Category)
# admin.site.register(News)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','slug','published_time','status']
    list_filter = ['status','created_time','published_time']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_time'
    search_fields = ['title','body']
    ordering = ['status','published_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Contact)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body','created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user','body']
    actions = ['disable_comment', 'active_comment']

    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def active_comment(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Comment, CommentAdmin)