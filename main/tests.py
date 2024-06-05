from django.test import TestCase

from main.forms import LoginForm
from main.models import Course, Comment


# Create your tests here.

class MyTestCase(TestCase):
    def setUp(self):
        print("setUp")
        self.project1 = Comment.objects.create(text='It is b')
        # self.project2 = Course.objects.create(name="Project 2",description="Project 2 dec",price=600)

    def test_setUp(self):
        y = 8 + 10
        # print(self.project1)
        self.assertEqual(y, 18)

    def test_tearDown(self):
        url = self.client.get("/course/")
        print(url)
        print(url.context['courses'])
        self.assertEqual(url.status_code, 200)
        self.assertEqual(self.project1.text, "It is beautiful course")

    def test_form(self):
        form = LoginForm(data={'username': 'admin', 'password': '8y!'})
        self.assertTrue(form.is_valid())

    def test_model(self):
        pass
