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
    instrument = models.TextField(default='')
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
    # 题号
    number = models.IntegerField(default=1)
    kind = models.TextField(default="SC")
    # 题干
    stem = models.TextField(default='')
    # 选项一文本
    choice_1 = models.TextField(default='')
    # 选项二文本
    choice_2 = models.TextField(default='')
    # 选项三文本
    choice_3 = models.TextField(default='')
    # 选项四文本
    choice_4 = models.TextField(default='')
    # 答案
    answer = models.TextField(default='')

    homework = models.ForeignKey(
        HomeworkPost,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='single_choice_question'
    )

    def __str__(self):
        return self.stem


class ReadingComprehensionQuestionPost(models.Model):
    number = models.IntegerField(default=1)
    kind = models.TextField(default="RC")
    essay = models.TextField(default='')

    stem_1 = models.TextField(default='')
    choice_1_1 = models.TextField(default='')
    choice_1_2 = models.TextField(default='')
    choice_1_3 = models.TextField(default='')
    choice_1_4 = models.TextField(default='')
    answer_1 = models.TextField(default='')

    stem_2 = models.TextField(default='')
    choice_2_1 = models.TextField(default='')
    choice_2_2 = models.TextField(default='')
    choice_2_3 = models.TextField(default='')
    choice_2_4 = models.TextField(default='')
    answer_2 = models.TextField(default='')

    stem_3 = models.TextField(default='')
    choice_3_1 = models.TextField(default='')
    choice_3_2 = models.TextField(default='')
    choice_3_3 = models.TextField(default='')
    choice_3_4 = models.TextField(default='')
    answer_3 = models.TextField(default='')

    stem_4 = models.TextField(default='')
    choice_4_1 = models.TextField(default='')
    choice_4_2 = models.TextField(default='')
    choice_4_3 = models.TextField(default='')
    choice_4_4 = models.TextField(default='')
    answer_4 = models.TextField(default='')

    stem_5 = models.TextField(default='')
    choice_5_1 = models.TextField(default='')
    choice_5_2 = models.TextField(default='')
    choice_5_3 = models.TextField(default='')
    choice_5_4 = models.TextField(default='')
    answer_5 = models.TextField(default='')

    stem_6 = models.TextField(default='')
    choice_6_1 = models.TextField(default='')
    choice_6_2 = models.TextField(default='')
    choice_6_3 = models.TextField(default='')
    choice_6_4 = models.TextField(default='')
    answer_6 = models.TextField(default='')

    homework = models.ForeignKey(
        HomeworkPost,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reading_comprehension_question'
    )

    def __str__(self):
        return self.essay[0:10]