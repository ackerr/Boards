from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import signup
from ..forms import SignUpForm


# Create your tests here.


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)  # 写错form表单

    def test_form_input(self):
        self.assertContains(self.response, '<input', 6)  # 5改为6，版本原因？？
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'zmj',
            'email': 'john@doe.com',
            'password1': 'zmjzmj123',
            'password2': 'zmjzmj123',  # 测试用数据必须正确
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    # 有效的注册，结束后跳转
    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    # 查看用户注册有没有保存在数据库
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
