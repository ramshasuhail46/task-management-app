from django.contrib import admin

# Register your models here.

from .models import User, DailyCheckin, Task, Notes


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'is_active',)
    ordering = ('email',)


class DailyCheckinAdmin(admin.ModelAdmin):
    model = DailyCheckin
    list_display = ('user', 'datetime_of_checkin')
    search_fields = ('user',)


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('task', 'created_at', 'user', 'assigned_by', 'rate',)
    search_fields = ('task', 'created_at', 'user', 'assigned_by', 'rate',)


class NotesAdmin(admin.ModelAdmin):
    model = Notes
    list_display = ('note', 'written_by', 'task',)
    search_fields = ('written_by', 'task',)


admin.site.register(User, UserAdmin)
admin.site.register(DailyCheckin, DailyCheckinAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Notes, NotesAdmin)
