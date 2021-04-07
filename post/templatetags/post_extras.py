from django import template
from ..models import Comment, Post

register = template.Library()

@register.inclusion_tag('post/last_comments.html')
def show_last_comments(count=5):
    latest_comments = Comment.objects.filter(active=True)[0:count]
    return {'latest_comments':latest_comments}


@register.inclusion_tag('post/last_posts.html')
def show_last_posts(count=5):
    last_posts = Post.objects.filter(active=True)[0:count]
    return {'last_posts':last_posts}