from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from django.http import Http404
from .forms import NewTopicForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count


# Create your views here.


def home(req):
    boards = Board.objects.all()

    return render(req, 'home.html', {'boards': boards})


def board_topics(req, pk):
    board = get_object_or_404(Board, id=pk)
    topics = board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)

    return render(req, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(req, pk):
    board = get_object_or_404(Board, pk=pk)
    if req.method == 'POST':
        form = NewTopicForm(req.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = req.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=req.user
            )

            return redirect('board_topics', pk=pk, topic_pk=topic.pk)

    else:
        form = NewTopicForm()
    return render(req, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(req, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(req, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(req, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = req.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    form = PostForm()
    return render(req, 'reply_topic.html', {'topic': topic, 'form': form})
