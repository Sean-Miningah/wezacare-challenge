from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from questions.models import User, Questions, Answers


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class UserAdmin(BaseUserAdmin):
    
    form = UserChangeForm 
    add_form = UserCreationForm 

    list_display =('id', 'email', 'username')
    list_filter=('username',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
    )

    add_fieldsets = (
        (None, {
          'classes': ('wide',),
          'fields': ('username', 'email', 'password1', 'password2')
        })
    )


class QuestionAdmin(admin.ModelAdmin):
    list_dislay = ('id', 'description', 'author')

    fieldsets = (
        (None, {
          'fields': ('id', 'description', 'author'),
        }),
    )

    add_fieldsets = (
        (None, {
          'fields': ('id', 'description', 'author'),
        })
    )


class AnswerAdmin(admin.ModelAdmin):
    list_dislay = ('id', 'description', 'question')

    fieldsets = (
        (None, {
          'fields': ('id', 'description', 'question'),
        }),
    )

    add_fieldsets = (
        (None, {
          'fields': ('id', 'description', 'question'),
        })
    )

admin.site.register(User, UserAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Answers, AnswerAdmin)
