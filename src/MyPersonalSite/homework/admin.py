from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(HomeworkPost)
admin.site.register(HomeworkColumn)
admin.site.register(BigQuestionPost)
admin.site.register(SmallQuestionPost)
admin.site.register(ChoicePost)
admin.site.register(AnswerPost)
admin.site.register(GradePost)