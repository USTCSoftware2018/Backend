from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, \
    UserCreationForm as BaseUserCreationForm

from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.list_display = (
            'actualname', 'organization', 'location', 'followers', 'is_staff', 'is_superuser'
        )


class UserAdmin(BaseUserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'actualname', 'organization', 'is_staff', 'is_superuser')
        self.search_fields = ('username', 'actualname', 'organization')
        self.form = UserChangeForm
        self.add_form = UserCreationForm

    fieldsets = BaseUserAdmin.fieldsets + (
        ('personal info',
         {'fields': ('portrait', 'actualname', 'nick_name', 'profile')}),
    )


admin.site.register(User, UserAdmin)