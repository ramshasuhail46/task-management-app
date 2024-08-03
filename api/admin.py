from django.contrib import admin

# Register your models here.

from .models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'is_active',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)

