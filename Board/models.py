from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # 自定义方法，返回需要的查询集合
    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=200)
    last_update = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)  # 浏览次数，默认为0

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.message)  # 取前30个字符？？
        return truncated_message.chars(30)
