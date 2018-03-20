from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..views import PostUpdateView
from ..models import Post, Board, Topic


class PostUpdateViewTestCase(TestCase):

    # 初始化各种信息
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = 'sdasd123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=user)
        self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })


# 继承初始化信息的类
class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):

    # 测试是否使用了login_required 装饰器登录才能修改，不然重定向
    def test_redirect(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


# 检验没有权限的人更改结果，404
class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    # 初始化另一个信息
    def setUp(self):
        super().setUp()
        username = 'zmj'
        password = 'zmjzmj123'
        user = User.objects.create_user(username=username, password=password, email='')
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)


class PostUpdateViewTests(PostUpdateViewTestCase):
    pass


class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    pass


class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    pass
