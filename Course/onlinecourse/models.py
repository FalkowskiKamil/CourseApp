import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings

class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username

class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation

class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    image = models.FileField(upload_to='course_images/', blank=True, null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Lesson Subject: " + self.title

class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=200, default = "Question text")
    grade_point = models.IntegerField(default=1)
    
    def is_get_score(self, selected_choices):
        correct_choices = self.choices.filter(is_correct=True)
        selected_choices = self.choices.filter(pk__in=selected_choices, is_correct=True)
        return selected_choices.count() == correct_choices.count()
    
    def __str__(self):
        return "Question to course: " + self.course.name + ", "+ \
                "Question content: " + self.question_text
   
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None, null=True, related_name='choices')
    choice_text = models.CharField(max_length=500, default="answer")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "Answer: " + self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, default=None)
    choice = models.ManyToManyField(Choice)