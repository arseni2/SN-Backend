from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model



MyUser = get_user_model()

'''
перенести сюда весь мой проект из пичарма
'''
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'userPhotos', 'username')

    #def clean_password2(self):
        # Check that the two password entries match
        #password1 = self.cleaned_data.get("password1")
        #password2 = self.cleaned_data.get("password2")
        #if password1 and password2 and password1 != password2:
            #raise forms.ValidationError("Passwords don't match")
        #return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin', 'first_name', 'userPhotos', 'username', 'full_name', 'slug', 'last_name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    save_as = True
    save_on_top = True
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'first_name', 'is_active', 'userPhotos', 'full_name', 'slug', 'last_name')
    list_filter = ('is_admin','first_name','is_active', 'slug')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'userPhotos', 'slug')}),
        ('Personal info', {'fields': ('first_name', 'username', 'full_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'slug', 'userPhotos', 'is_admin', 'is_active', 'year', 'country', 'username', 'last_name', 'first_name', 'status', 'birth_date', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
