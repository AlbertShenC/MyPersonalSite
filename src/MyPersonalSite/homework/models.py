from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class HomeworkColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class HomeworkPost(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    instrument = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    column = models.ForeignKey(
        HomeworkColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='homework'
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class SingleChoiceQuestionPost(models.Model):
    # 题干
    stem = models.TextField()
    # 选项一文本
    choice_1 = models.TextField()
    # 选项二文本
    choice_2 = models.TextField()
    # 选项三文本
    choice_3 = models.TextField()
    # 选项四文本
    choice_4 = models.TextField()
    # 答案
    answer = models.TextField()

    homework = models.ForeignKey(
        HomeworkPost,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='single_choice_question'
    )

    def __str__(self):
        return self.stem
