from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from itertools import chain
from operator import attrgetter
from .models import *
from .forms import *

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
    small_questions = SmallQuestionPost.objects.filter(big_question=big_questions[0].id)
    for big_question in big_questions[1:]:
        small_questions = small_questions | SmallQuestionPost.objects.filter(big_question=big_question.id)
    choices = ChoicePost.objects.filter(small_question=small_questions[0].id)
    for small_question in small_questions[1:]:
        choices = choices | ChoicePost.objects.filter(small_question=small_question.id)

    # single_choice_question = SingleChoiceQuestionPost.objects.filter(homework=homework_id)
    # reading_comprehension_quesiton = ReadingComprehensionQuestionPost.objects.filter(homework=homework_id)
    # questions = sorted(chain(single_choice_question, reading_comprehension_quesiton),
    #                    key=attrgetter('number'), reverse=False)

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
        homework_post_form = HomeworkPostForm(request.POST)
        if homework_post_form.is_valid():
            new_homework = homework_post_form.save(commit=False)
            new_homework.teacher = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_homework.column = HomeworkColumn.objects.get(id=request.POST['column'])
            new_homework.save()
            return redirect('homework:homework_list')
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        homework_post_form = HomeworkPostForm()
        columns = HomeworkColumn.objects.all()
        context = {'homework_post_form': homework_post_form, 'columns': columns}
        return render(request, 'homework/create_homework.html', context)


@login_required(login_url='/user/login/')
def homework_delete(request, homework_id):
    if request.method == 'POST':
        homework = HomeworkPost.objects.get(id=homework_id)
        if request.user != homework.teacher:
            return HttpResponse("抱歉，你无权删除这篇作业。")
        homework.delete()
        return redirect('homework:homework_list')
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/user/login/')
def homework_update(request, homework_id):
    homework = HomeworkPost.objects.get(id=homework_id)
    if request.method == 'POST':
        homework_post_form = HomeworkPostForm(request.POST)
        if homework_post_form.is_valid():
            homework.title = request.POST['title']
            homework.instrument = request.POST['instrument']
            if request.POST['column'] != 'none':
                homework.column = HomeworkColumn.objects.get(id=request.POST['column'])
            homework.save()
            return redirect('homework:homework_list')
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        homework_post_form = HomeworkPostForm()
        columns = HomeworkColumn.objects.all()
        context = {
            'homework_post_form': homework_post_form,
            'columns': columns,
            'homework': homework
        }
        return render(request, 'homework/update_homework.html', context)


# @login_required(login_url='/user/login/')
# def create_single_choice_question(request, homework_id):
#     if request.method == 'POST':
#         single_choice_question_form = SingleChoiceQuestionPostForm(request.POST)
#         if single_choice_question_form.is_valid():
#             new_single_choice_question = single_choice_question_form.save(commit=False)
#             new_single_choice_question.homework = HomeworkPost.objects.get(id=homework_id)
#             new_single_choice_question.save()
#             return redirect(reverse('homework:homework_detail', args=[homework_id]))
#         else:
#             return HttpResponse('表单内容有误，请重新填写。')
#     else:
#         single_choice_question_form = SingleChoiceQuestionPostForm()
#         context = {
#             'single_choice_question_form': single_choice_question_form
#         }
#         return render(request, 'homework/create_single_choice_question.html', context)
#
#
# @login_required(login_url='/user/login/')
# def update_single_choice_question(request, question_id):
#     single_choice_question = SingleChoiceQuestionPost.objects.get(id=question_id)
#     if request.method == 'POST':
#         single_choice_question_form = SingleChoiceQuestionPostForm(request.POST)
#         if single_choice_question_form.is_valid():
#             single_choice_question.stem = request.POST['stem']
#             single_choice_question.choice_1 = request.POST['choice_1']
#             single_choice_question.choice_2 = request.POST['choice_2']
#             single_choice_question.choice_3 = request.POST['choice_3']
#             single_choice_question.choice_4 = request.POST['choice_4']
#             single_choice_question.answer = request.POST['answer']
#             single_choice_question.save()
#             return redirect(reverse('homework:homework_detail', args=[single_choice_question.homework.id]))
#         else:
#             return HttpResponse('表单内容有误，请重新填写。')
#     else:
#         single_choice_question_form = SingleChoiceQuestionPostForm()
#         context = {
#             'single_choice_question_form': single_choice_question_form,
#             'single_choice_question': single_choice_question
#         }
#         return render(request, 'homework/update_single_choice_question.html', context)
#
#
# @login_required(login_url='/user/login/')
# def delete_single_choice_question(request, question_id):
#     if request.method == 'POST':
#         single_choice_question = SingleChoiceQuestionPost.objects.get(id=question_id)
#         if request.user != single_choice_question.homework.teacher:
#             return HttpResponse("抱歉，你无权删除这篇作业。")
#         single_choice_question.delete()
#         return redirect(reverse('homework:homework_detail', args=[single_choice_question.homework.id]))
#     else:
#         return HttpResponse("仅允许post请求")
#
#
# @login_required(login_url='/user/login/')
# def create_reading_comprehension_question(request, homework_id):
#     if request.method == 'POST':
#         reading_comprehension_question_form = ReadingComprehensionQuestionPostForm(request.POST)
#         if reading_comprehension_question_form.is_valid():
#             new_reading_comprehension_question = reading_comprehension_question_form.save(commit=False)
#             new_reading_comprehension_question.homework = HomeworkPost.objects.get(id=homework_id)
#             new_reading_comprehension_question.save()
#             return redirect(reverse('homework:homework_detail', args=[homework_id]))
#         else:
#             return HttpResponse('表单内容有误，请重新填写。')
#     else:
#         reading_comprehension_question_form = ReadingComprehensionQuestionPostForm()
#         context = {
#             'single_choice_question_form': reading_comprehension_question_form
#         }
#         return render(request, 'homework/create_reading_comprehension_question.html', context)