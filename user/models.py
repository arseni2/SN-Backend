from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from django.utils.text import slugify


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, last_name=None, userPhotos=None, first_name=None, country=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            userPhotos=userPhotos,
            first_name=first_name,
            last_name=last_name,
            country=country,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        arsenij633@gmail.com
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    birth_date = models.DateField(null=True)
    status = models.CharField(max_length=200, default=' ', null=True)
    first_name = models.TextField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200)
    country = models.CharField(max_length=200, null=True)
    year = models.PositiveIntegerField(null=True)
    is_active = models.BooleanField(default=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)
    userPhotos = models.ImageField(upload_to='userPhotos')
    full_name = models.CharField(max_length=256, null=True)
    slug = models.SlugField(unique=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @staticmethod
    def authenticate(email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(id_):
        try:
            return User.objects.get(pk=id_)
        except User.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.first_name)+str(self.last_name)+str(self.id))
        super(User, self).save(*args, **kwargs)