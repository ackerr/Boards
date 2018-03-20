from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Board, Topic, Post
from django.urls import reverse, resolve
from ..views import reply_topic


class ReplyTopicTestCase(TestCase):

    # 初始化一个Post
    def setUp(self):
        self.board = Board.objects.create(name='django', description='django is good.')
        self.username = 'zmj'
        self.password = 'zmjzmj123'
        user = User.objects.create(username=self.username, password=self.password, email='zmj@12.com')
        self.topic = Topic.objects.create(subject='python', starter=user, board=self.board)
        Post.objects.create(message='this is a test', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    pass


class ReplyTopicTests(ReplyTopicTestCase):
    pass


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def test_redirect(self):
        url = reverse('topic_posts',kwargs={'pk':self.board.pk,'topic_pk':self.topic.pk})
        topic_posts_url='{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response,topic_posts_url)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    pass
