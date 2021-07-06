from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter
from allauth.utils import (email_address_exists,
                           get_username_max_length)

User = get_user_model()


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = "__all__"


from rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    userPhotos = serializers.ImageField(required=True)
    password1 = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if True:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'userPhotos': self.validated_data.get('userPhotos', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'country': self.validated_data.get('country', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        user.userPhotos = self.cleaned_data.get('userPhotos')
        user.country = self.cleaned_data.get('country')
        user.username = str(self.cleaned_data.get('first_name'))
        user.full_name = str(self.cleaned_data.get('first_name'))+' '+str(self.cleaned_data.get('last_name'))
        user.save()
        return user
