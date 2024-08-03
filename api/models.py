from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from datetime import datetime
from django.utils import timezone


# Create your models here.


class CustomUserManager(UserManager):
    """
    Custom User Manager for setting email and password
    """

    def _create_user(self, email, password, username, **extra_fields):
        """
        Connect method docstring: Brief description of the connect method.
        """
        if not email:
            raise ValueError("you have not provided a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User-Model
    """

    options = (
        ('Employee', 'employee'),
        ('Manager', 'manager'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    otp = models.IntegerField(default=0000)
    role = models.CharField(
        max_length=200, choices=options, default='Employee')
    manager = models.ForeignKey('self', null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='subordinates')

    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        """

        """
        return self.email


class DailyCheckin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    datetime_of_checkin = models.DateTimeField(default=timezone.now)


class Task(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1, '1'
        TWO = 2, '2'
        THREE = 3, '3'
        FOUR = 4, '4'
        FIVE = 5, '5'

    task = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='assigned_to')
    assigned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='assigned_by')
    rate = models.IntegerField(choices=Rating.choices, default=Rating.ONE)


class Notes(models.Model):
    note = models.TextField()
    written_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False)
