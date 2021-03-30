from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib import admin


# disable the left sidebar
admin.autodiscover()
admin.site.enable_nav_sidebar = False


# don't show group in admin
admin.site.unregister(Group)


# change the admin user form
class CustomUserAdmin(UserAdmin):
    prepopulated_fields = {'username': ('first_name', 'last_name',)}
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_staff',), }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2',),
        }),
        (_('Permissions'), {'fields': ('is_staff',), }),
    )
    list_filter = ()
    search_fields = ()
    list_display = ('username', 'email', 'first_name', 'last_name')

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if obj.is_staff:
            obj.is_superuser = True
        obj.save()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
