from django.contrib import admin

from .models import Tasks

# Register your models here


class TasksAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "due_date", "content")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Tasks, TasksAdmin)

