from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class SchoolClassPost(models.Model):
    name = models.TextField(default='')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school_class = models.ForeignKey(SchoolClassPost, on_delete=models.CASCADE,
                                     related_name='profile', null=True,
                                     blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    # 考号
    examination_number = models.CharField(max_length=10, blank=True)
    # 各种题目默认分数
    default_choice_score = models.IntegerField(default=2, blank=True)
    default_reading_comprehension_score = models.IntegerField(default=3, blank=True)
    default_cloze_score = models.IntegerField(default=2, blank=True)

    def __str__(self):
        return 'user{}'.format(self.user.username)
