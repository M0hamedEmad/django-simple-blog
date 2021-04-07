from django.forms import ModelForm
from .models import Post, Comment, Category

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'categories', 'photo')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')