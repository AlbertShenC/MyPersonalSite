from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


# 栏目表
class HomeworkColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 作业表
class HomeworkPost(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homeworks')
    column = models.ForeignKey(HomeworkColumn, on_delete=models.CASCADE, related_name='homeworks')
    title = models.TextField(default='')
    instrument = models.TextField(default='', blank=True)
    total_time_minute = models.TextField(default='')

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


# 大题表：一道单选/一道多选/一篇阅读/一篇完型
class BigQuestionPost(models.Model):
    homework = models.ForeignKey(HomeworkPost, on_delete=models.CASCADE, related_name='big_questions')
    number = models.IntegerField(default=1)
    kind = models.TextField(default='SingleChoice')
    essay = models.TextField(default='', blank=True)

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return 'Homework {0}-{1}.{2}'.format(str(self.homework.id), str(self.number), self.essay[:10])


# 小题表：一道单选/一道多选，阅读/完型的一小道题
class SmallQuestionPost(models.Model):
    big_question = models.ForeignKey(BigQuestionPost, on_delete=models.CASCADE, related_name='small_questions')
    number_offset = models.IntegerField(default=0)
    stem = models.TextField(default='', blank=True)
    reference_answer = models.TextField(default='', blank=True)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ('number_offset',)

    def __str__(self):
        return 'Question {0}-{1}.{2}'.format(str(self.big_question.id), str(self.number_offset), self.stem[:10])


# 选项表：一个选项
class ChoicePost(models.Model):
    small_question = models.ForeignKey(SmallQuestionPost, on_delete=models.CASCADE, related_name='choices')
    # 选项A、B、C等
    choice_stem = models.CharField(default='A', max_length=1)
    # 选项文本
    choice_text = models.TextField(default='')

    class Meta:
        ordering = ('choice_stem',)

    def __str__(self):
        return '{0}.{1}'.format(self.choice_stem, self.choice_text[:10])


# 答案表
class AnswerPost(models.Model):
    small_question = models.ForeignKey(SmallQuestionPost, on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField(default='', blank=True)
    final_grade = models.IntegerField(default=0)

    class Meta:
        ordering = ('small_question',)

    def __str__(self):
        return self.answer_text[:10]


# 成绩表
class GradePost(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    homework = models.ForeignKey(HomeworkPost, on_delete=models.CASCADE, related_name='grades')
    final_grade = models.IntegerField(default=0)

    class Meta:
        ordering = ('homework',)

    def __str__(self):
        return self.student
