from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from itertools import chain
from operator import attrgetter
from .models import *
from .forms import *
from user.models import SchoolClassPost

# Create your views here.


def homework_list(request):
    search = request.GET.get('search')
    column = request.GET.get('column')

    homework_list = HomeworkPost.objects.all()

    if search:
        homework_list = homework_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    if column is not None and column.isdigit():
        homework_list = homework_list.filter(column=column)

    paginator = Paginator(homework_list, 9)
    page = request.GET.get('page')
    homeworks = paginator.get_page(page)

    context = {
        'homeworks': homeworks,
        'search': search,
    }

    return render(request, 'homework/list.html', context)


def homework_main(request):
    return redirect('homework:homework_list')


def homework_detail(request, homework_id):
    homework = HomeworkPost.objects.get(id=homework_id)
    big_questions = BigQuestionPost.objects.filter(homework=homework_id)
    small_questions = SmallQuestionPost.objects.filter(big_question__homework__id=homework_id)
    choices = ChoicePost.objects.filter(small_question__big_question__homework__id=homework_id)

    context = {
        'homework': homework,
        'big_questions': big_questions,
        'small_questions': small_questions,
        'choices': choices
    }
    return render(request, 'homework/detail.html', context)


@login_required(login_url='/user/login/')
def homework_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        column = request.POST.get('column')
        instrument = request.POST.get('instrument')
        total_time_minute = int(request.POST.get('total_time_minute'))

        if title == '':
            return HttpResponse('标题不能为空')
        if total_time_minute < 0:
            return HttpResponse('完成时间不能小于0')

        HomeworkPost(teacher=request.user, title=title,
                     column=HomeworkColumn.objects.get(id=column),
                     instrument=instrument, total_time_minute=total_time_minute).save()
        return redirect('homework:homework_list')
    else:
        columns = HomeworkColumn.objects.all()
        context = {
            'columns': columns
        }
        return render(request, 'homework/update_homework.html', context)


@login_required(login_url='/user/login/')
def homework_update(request, homework_id):
    homework = HomeworkPost.objects.get(id=homework_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        column = request.POST.get('column')
        instrument = request.POST.get('instrument')
        total_time_minute = int(request.POST.get('total_time_minute'))

        if title == '':
            return HttpResponse('标题不能为空')
        if total_time_minute < 0:
            return HttpResponse('完成时间不能小于0')

        homework = HomeworkPost.objects.get(id=homework_id)
        homework.title = title
        homework.column = HomeworkColumn.objects.get(id=column)
        homework.instrument = instrument
        homework.total_time_minute = total_time_minute
        homework.save()
        return redirect('homework:homework_list')
    else:
        columns = HomeworkColumn.objects.all()
        context = {
            'columns': columns,
            'homework': homework
        }
        return render(request, 'homework/update_homework.html', context)


@login_required(login_url='/user/login/')
def homework_delete(request, homework_id):
    if request.method == 'POST':
        homework = HomeworkPost.objects.get(id=homework_id)
        if request.user != homework.teacher:
            return JsonResponse({
                "code": "No",
                "message": "抱歉，你无权删除此题。"
            })
        homework.delete()
        return JsonResponse({
            "code": "Yes",
            "new_href": reverse('homework:homework_list')
        })
    else:
        return JsonResponse({
            "code": "No",
            "message": "仅允许post请求。"
        })


def calculate_total_grade(homework_id, student_id):
    answers = AnswerPost.objects.filter(small_question__big_question__homework=homework_id,
                                        student=student_id).values('final_grade')
    total_grade = 0
    for answer in answers:
        total_grade = total_grade + answer['final_grade']
    return total_grade


@login_required(login_url='/user/login/')
def submit_homework(request, homework_id):
    if request.method == 'POST':
        student = request.user
        print(student)
        for answer in request.POST.lists():
            if answer[0].isdigit():
                small_question = SmallQuestionPost.objects.get(id=int(answer[0]))
                if AnswerPost.objects.filter(small_question=small_question.id,
                                             student=student.id):
                    new_answer = AnswerPost.objects.get(small_question=small_question.id,
                                                        student=student.id)
                    new_answer.answer_text = answer[1][0]
                    new_answer.save()
                else:
                    new_answer = AnswerPost(small_question=small_question,
                                            student=student,
                                            answer_text=answer[1][0])
                    new_answer.save()
        if not GradePost.objects.filter(student=student.id, homework=homework_id):
            grade = GradePost(student=User.objects.get(id=student.id),
                              homework=HomeworkPost.objects.get(id=homework_id))
            grade.save()
        return redirect('homework:homework_list')
    else:
        return HttpResponse('仅支持POST请求。')


@login_required(login_url='/user/login/')
def mark_homework(request, homework_id, student_id):
    if request.method == 'POST':
        for mark_grade in request.POST.lists():
            if mark_grade[0].isdigit():
                answer = AnswerPost.objects.get(small_question=int(mark_grade[0]), student=student_id)
                answer.final_grade = int(mark_grade[1][0])
                answer.save()
        if GradePost.objects.filter(student=student_id, homework=homework_id):
            grade = GradePost.objects.get(student=student_id, homework=homework_id)
        else:
            grade = GradePost(student=User.objects.get(id=student_id),
                              homework=HomeworkPost.objects.get(id=homework_id))
        grade.final_grade = calculate_total_grade(homework_id, student_id)
        grade.save()

        return redirect(reverse('homework:mark_homework', args=[homework_id, student_id]))
    elif request.method == 'GET':
        student = User.objects.get(id=student_id)
        homework = HomeworkPost.objects.get(id=homework_id)
        answers = AnswerPost.objects.filter(small_question__big_question__homework=homework_id,
                                            student=student_id)
        context = {
            'student': student,
            'homework': homework,
            'answers': answers
        }
        return render(request, 'homework/mark_student_homework_grade.html', context)


@login_required(login_url='/user/login/')
def homework_grade(request, homework_id, student_id):
    if request.method == 'GET':
        student = User.objects.get(id=student_id)
        homework = HomeworkPost.objects.get(id=homework_id)
        answers = AnswerPost.objects.filter(small_question__big_question__homework=homework_id,
                                            student=student_id)
        total_grade = GradePost.objects.get(student=student_id, homework=homework_id)
        context = {
            'student': student,
            'homework': homework,
            'answers': answers,
            'total_grade': total_grade
        }
        return render(request, 'homework/student_homework_grade.html', context)
    else:
        return HttpResponse('仅支持GET请求。')


@login_required(login_url='/user/login/')
def school_class_homework(request, school_class_id, homework_id):
    if request.method == 'GET':
        grades = GradePost.objects.filter(student__profile__school_class=school_class_id,
                                          homework=homework_id)
        school_class = SchoolClassPost.objects.get(id=school_class_id)
        context = {
            'grades': grades,
            'school_class': school_class
        }
        return render(request, 'homework/school_class_homework.html', context)
    else:
        return HttpResponse('仅支持GET请求。')


@login_required(login_url='/user/login/')
def homework_overview(request, homework_id):
    if request.method == 'GET':
        grades = GradePost.objects.filter(homework=homework_id)
        context = {
            'grades': grades,
        }
        return render(request, 'homework/school_class_homework.html', context)
    else:
        return HttpResponse('仅支持GET请求。')


@login_required(login_url='/user/login/')
def delete_big_question(request, big_question_id):
    if request.method == 'POST':
        big_question = BigQuestionPost.objects.get(id=big_question_id)
        homework_id = big_question.homework.id
        if request.user != big_question.homework.teacher:
            return JsonResponse({
                "code": "No",
                "message": "抱歉，你无权删除此题。"
            })
        big_question.delete()
        return JsonResponse({
            "code": "Yes",
            "new_href": reverse("homework:homework_detail", args=[homework_id])
        })
    else:
        return JsonResponse({
            "code": "No",
            "message": "仅允许post请求"
        })


@login_required(login_url='/user/login/')
def delete_small_question(request, small_question_id):
    if request.method == 'POST':
        small_question_id = SmallQuestionPost.objects.get(id=small_question_id)
        homework_id = small_question_id.big_question.homework.id
        if request.user != small_question_id.big_question.homework.teacher:
            return JsonResponse({
                "code": "No",
                "message": "抱歉，你无权删除此题。"
            })
        small_question_id.delete()
        return JsonResponse({
            "code": "Yes",
            "new_href": reverse("homework:homework_detail", args=[homework_id])
        })
    else:
        return JsonResponse({
            "code": "No",
            "message": "仅允许post请求"
        })


@login_required(login_url='/user/login/')
def create_choice_question(request, homework_id):
    if request.method == 'POST':
        number = request.POST.get('number')
        stem = request.POST.get('stem')
        choice_number = int(request.POST.get('choice_number'))
        reference_answer = request.POST.get('reference_answer')
        score = request.POST.get('score')

        new_big_question = BigQuestionPost(homework=HomeworkPost.objects.get(id=homework_id),
                                           number=number, kind='SingleChoice')
        new_big_question.save()
        new_small_question = SmallQuestionPost(big_question=new_big_question, stem=stem,
                                               reference_answer=reference_answer,
                                               score=score)
        new_small_question.save()
        for i in range(0, choice_number):
            ChoicePost(small_question=new_small_question,
                       choice_stem=chr(ord('A') + i),
                       choice_text=request.POST.get(chr(ord('A') + i))).save()

        return redirect(reverse('homework:homework_detail', args=[homework_id]))
    else:
        return render(request, 'homework/update_choice_question.html')


@login_required(login_url='/user/login/')
def update_choice_question(request, big_question_id):
    if request.method == 'POST':
        number = request.POST.get('number')
        stem = request.POST.get('stem')
        choice_number = int(request.POST.get('choice_number'))
        reference_answer = request.POST.get('reference_answer')
        score = request.POST.get('score')

        big_question = BigQuestionPost.objects.get(id=big_question_id)
        big_question.number = number
        big_question.save()

        small_question = SmallQuestionPost.objects.get(big_question=big_question)
        small_question.stem = stem
        small_question.reference_answer = reference_answer
        small_question.score = score
        small_question.save()

        ChoicePost.objects.filter(small_question=small_question.id).delete()

        for i in range(0, choice_number):
            ChoicePost(small_question=small_question,
                       choice_stem=chr(ord('A') + i),
                       choice_text=request.POST.get(chr(ord('A') + i))).save()

        return redirect(reverse('homework:homework_detail', args=[big_question.homework.id]))
    else:
        big_question = BigQuestionPost.objects.get(id=big_question_id)
        small_question = SmallQuestionPost.objects.get(big_question=big_question_id)
        choices = ChoicePost.objects.filter(small_question__big_question=big_question_id)
        context = {
            'big_question': big_question,
            'small_question': small_question,
            'choices': choices
        }
        return render(request, 'homework/update_choice_question.html', context)


@login_required(login_url='/user/login/')
def create_reading_comprehension_question(request, homework_id):
    if request.method == 'POST':
        number = request.POST.get('number')
        essay = request.POST.get('essay')

        new_big_question = BigQuestionPost(homework=HomeworkPost.objects.get(id=homework_id),
                                           number=number, kind='ReadingComprehension',
                                           essay=essay)
        new_big_question.save()

        return redirect(reverse('homework:create_reading_comprehension_small_question', args=[new_big_question.id]))
    else:
        return render(request, 'homework/create_reading_comprehension_question.html')


@login_required(login_url='/user/login/')
def update_reading_comprehension_question(request, big_question_id):
    if request.method == 'POST':
        number = request.POST.get('number')
        essay = request.POST.get('essay')

        big_question = BigQuestionPost.objects.get(id=big_question_id)
        big_question.number = number
        big_question.essay = essay
        big_question.save()

        return redirect(reverse('homework:homework_detail', args=[big_question.homework.id]))
    else:
        big_question = BigQuestionPost.objects.get(id=big_question_id)
        context = {
            'big_question': big_question
        }
        return render(request, 'homework/create_reading_comprehension_question.html', context)


@login_required(login_url='/user/login/')
def create_reading_comprehension_small_question(request, big_question_id):
    if request.method == 'POST':
        number_offset = request.POST.get('number_offset')
        stem = request.POST.get('stem')
        choice_number = int(request.POST.get('choice_number'))
        reference_answer = request.POST.get('reference_answer')
        score = request.POST.get('score')

        new_small_question = SmallQuestionPost(big_question=BigQuestionPost.objects.get(id=big_question_id),
                                               number_offset=number_offset, stem=stem,
                                               reference_answer=reference_answer,
                                               score=score)
        new_small_question.save()
        for i in range(0, choice_number):
            ChoicePost(small_question=new_small_question,
                       choice_stem=chr(ord('A') + i),
                       choice_text=request.POST.get(chr(ord('A') + i))).save()

        if request.POST.get('add_new_question') == '1':
            return render(request, 'homework/create_reading_comprehension_small_question.html')
        return redirect(reverse('homework:homework_detail', args=[new_small_question.big_question.homework.id]))
    else:
        return render(request, 'homework/create_reading_comprehension_small_question.html')


@login_required(login_url='/user/login/')
def create_cloze_question(request, homework_id):
    if request.method == 'POST':
        number = request.POST.get('number')
        essay = request.POST.get('essay')

        new_big_question = BigQuestionPost(homework=HomeworkPost.objects.get(id=homework_id),
                                           number=number, kind='Cloze',
                                           essay=essay)
        new_big_question.save()

        return redirect(reverse('homework:create_cloze_small_question', args=[new_big_question.id]))
    else:
        return render(request, 'homework/create_reading_comprehension_question.html')


@login_required(login_url='/user/login/')
def create_cloze_small_question(request, big_question_id):
    if request.method == 'POST':
        number_offset = request.POST.get('number_offset')
        choice_number = int(request.POST.get('choice_number'))
        reference_answer = request.POST.get('reference_answer')
        score = request.POST.get('score')

        new_small_question = SmallQuestionPost(big_question=BigQuestionPost.objects.get(id=big_question_id),
                                               number_offset=number_offset,
                                               reference_answer=reference_answer,
                                               score=score)
        new_small_question.save()
        for i in range(0, choice_number):
            ChoicePost(small_question=new_small_question,
                       choice_stem=chr(ord('A') + i),
                       choice_text=request.POST.get(chr(ord('A') + i))).save()

        if request.POST.get('add_new_question') == '1':
            return render(request, 'homework/create_cloze_small_question.html')
        return redirect(reverse('homework:homework_detail', args=[new_small_question.big_question.homework.id]))
    else:
        return render(request, 'homework/create_cloze_small_question.html')
