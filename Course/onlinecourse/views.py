from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Course, Enrollment, Question, Choice, Submission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
logger = logging.getLogger(__name__)

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)

def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'

def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))

def submit(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    selected_choice = []
    
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            choice_id = int(value)
            selected_choice.append(Choice.objects.get(id=choice_id))
    
    submission.choice.set(selected_choice)
    return redirect('onlinecourse:show_exam_result', course_id=course_id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = Course.objects.get(id=course_id)
    submission = Submission.objects.get(id=submission_id)
    selected_choice_ids = list(submission.choice.all().values_list('id', flat=True))
    question_results = {}
    total_score = 0
    for question in course.questions.all():
        selected_ids = []
        choice_all = []
        choicen=None
        correct_choice = None
        
        for choice in question.choices.all():
            choice_all.append(choice.choice_text)
            
            if choice.id in selected_choice_ids:
                selected_ids.append(choice.id)
                choicen = choice.choice_text
                
                if choice.is_correct:
                    total_score += question.grade_point
                    correct_choice=choice.choice_text
            
            question_results[question.id] = {
                'question': question.question_text,
                'choice_all':choice_all,
                'choicen':choicen,
                'correct_choice':correct_choice,
                'is_correct': question.is_get_score(selected_ids),
                }
            
        while correct_choice is None and total_score == 0:
            for choice in question.choices.all():
                if choice.is_correct:
                    correct_choice = choice.choice_text
                    break  
            question_results[question.id] = {
                'question': question.question_text,
                'choice_all':choice_all,
                'choicen':choicen,
                'correct_choice':correct_choice,
                'is_correct': question.is_get_score(selected_ids),
                }

    # Calculate the passing score
    passing_score = sum(question.grade_point for question in course.questions.all()) / 2
    
    # Check if the user passed or failed the exam
    max_point = sum(question.grade_point for question in course.questions.all())
    # Add the course, selected_ids, and grade to context for rendering HTML page
    context = {
        'question_results': question_results,
        'total_score': total_score,
        'passing_score': passing_score,
        'max_point': max_point,
        'course': course_id,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context=context)