from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Topic, Post
from ..views import PostListView


class TopicPostTests(TestCase):
    # 初始化一个post
    def setUp(self):
        board = Board.objects.create(name='Django', description='Django board.')
        user = User.objects.create(username='zmj', email='zmj@12.com', password='123')
        topic = Topic.objects.create(subject='Test', board=board, starter=user)
        Post.objects.create(message='this is a test', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    # 判断状态码
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # ？？
    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)
