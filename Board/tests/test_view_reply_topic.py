from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Board, Topic, Post
from django.urls import reverse, resolve
from ..views import reply_topic


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='django', description='django is good.')
        self.username = 'zmj'
        self.password = '123'
        user = User.objects.create(username=self.username, password=self.password, email='zmj@12.com')
        self.topic = Topic.objects.create(subject='python', starter=user, board=self.board)
        Post.objects.create(message='this is a test', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    pass


class ReplyTopicTests(ReplyTopicTestCase):
    pass


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    pass


class InvalidReplyTopicTests(ReplyTopicTestCase):
    pass
