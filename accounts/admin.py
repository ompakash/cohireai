from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','password','type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),   
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(CustomUser,CustomUserAdmin)


class OrganizationAdditionalInline(admin.TabularInline):
    model = OrganizationAdditional
class OrganizationAdmin(admin.ModelAdmin):
    inlines = (
        OrganizationAdditionalInline,)
admin.site.register(OrganizationAdditional)
admin.site.register(Organization, OrganizationAdmin)


class EmployeeAdditionalInline(admin.TabularInline):
    model = EmployeeAdditional
class EmployeeAdmin(admin.ModelAdmin):
    inlines = (
        EmployeeAdditionalInline,)
admin.site.register(EmployeeAdditional)
admin.site.register(Employee, EmployeeAdmin)