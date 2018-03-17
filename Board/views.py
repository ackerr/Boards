from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from django.http import Http404
from .forms import NewTopicForm
from django.contrib.auth.models import User


# Create your views here.


def home(req):
    data = Board.objects.all()
    return render(req, 'home.html', {'data': data})


def board_topics(req, pk):
    board = get_object_or_404(Board, id=pk)
    topic = board.topics.all()
    return render(req, 'topics.html', {'board': board, 'topic': topic})


def new_topic(req, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()

    if req.method == 'POST':
        form = NewTopicForm(req.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )

            return redirect('board_topics', pk=board.pk)

    else:
        form = NewTopicForm()
    return render(req, 'new_topic.html', {'board': board, 'form': form})
