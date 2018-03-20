from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from django.http import Http404
from .forms import NewTopicForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
# Create your views here.


class BoardListView(ListView):
    model = Board
    template_name = 'home.html'
    context_object_name = 'boards'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key,False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
def new_topic(req, pk):
    board = get_object_or_404(Board, id=pk)
    if req.method == 'POST':
        form = NewTopicForm(req.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = req.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=req.user
            )

            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)

    else:
        form = NewTopicForm()
    return render(req, 'new_topic.html', {'board': board, 'form': form})


# def topic_posts(req, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(req, 'topic_posts.html', {'topic': topic})


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

            topic.last_update = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts',kwargs={'pk':pk,'topic_pk':topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    form = PostForm()
    return render(req, 'reply_topic.html', {'topic': topic, 'form': form})


# def new_post(req):
#     if req.method == 'POST':
#         form = PostForm(req.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#     else:
#         form = PostForm()
#     return render(req,'new_post.html',{'form':form})


# CBV
# class NewPostView(View):
#     def render(self,req):
#         return render(req,'new_topic.html',{'form':self.form})
#
#     def get(self,req):
#         self.form = PostForm()
#         return self.render(req)
#
#     def post(self,req):
#         self.form = PostForm(req.POST)
#         if self.form.is_valid():
#             self.form.save()
#             return redirect('post_list')
#         return self.render(req)


# GCBV 创建视图
class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')  # 反向获取url??
    template_name = 'new_topic.html'


# 更新视图
@method_decorator(login_required, name='dispatch')  # CBV 视图的内置登录验证装饰器调用
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'  # 用于识别关键字参数，检索后对象的名称，与url.py相识
    context_object_name = 'post'

    # 重写UpdateView 中的get_queryset 只有创建者是登录用户本人时才能修改
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

# def home(req):
#     boards = Board.objects.all()
#     return render(req, 'home.html', {'boards': boards})


# def board_topics(req, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
#     page = req.GET.get('page',1)
#     paginator = Paginator(queryset,15)
#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         topics = paginator.page(1)
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)
#     return render(req, 'topics.html', {'board': board, 'topics': topics})
