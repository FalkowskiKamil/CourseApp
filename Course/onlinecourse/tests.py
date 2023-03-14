from django.test import TestCase, Client
import unittest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *

class TestOnlinecourse(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='This is a test course.',
            image='course_images/test_course.png',
            total_enrollment=0
        )

        self.question = Question.objects.create(
            course = self.course,
            question_text = "Test choice",
            grade_point = 5,
        )


    def test_course_list_view(self):
        response = self.client.get(reverse('onlinecourse:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/course_list_bootstrap.html')
        self.assertContains(response, self.course.name)

    def test_course_detail_view(self):
        response = self.client.get(reverse('onlinecourse:course_details', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/course_detail_bootstrap.html')
        self.assertContains(response, self.course.name)

    def test_exam(self):
        response = self.client.get(reverse('onlinecourse:exam', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onlinecourse/exam.html')
        self.assertTrue(response, self.course.questions.all()[0])


if __name__=='__main__':
	unittest.main()