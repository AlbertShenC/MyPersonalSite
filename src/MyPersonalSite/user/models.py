from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    examination_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)