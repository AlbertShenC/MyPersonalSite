from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(HomeworkPost)
admin.site.register(HomeworkColumn)
admin.site.register(SingleChoiceQuestionPost)
admin.site.register(ReadingComprehensionQuestionPost)