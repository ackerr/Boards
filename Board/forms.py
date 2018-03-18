from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        label='内容',
        widget=forms.Textarea(attrs={'row': 5, 'placeholder': '说点什么吧!'}),
        max_length=4000,
        help_text='最大长度为4000',
        error_messages={'required': '不能为空'}  # 修改字段错误信息
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']
        labels = {
            'subject': '话题',
        }
        error_messages = {
            'subject': {'required': '不能为空'},  # 修改继承字段错误信息
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
