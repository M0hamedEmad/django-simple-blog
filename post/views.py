from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required 

from .models import Post, Comment
from .forms import PostForm, CommentForm
from .decorators import allowed_users


# Utilities
def same_user(request, post):
    if request.user == post.author or request.user.groups.filter(name='admin').count() != 0:
        return True
    
    return False

def home(request):
    posts = Post.objects.filter(active=True)
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts':posts,
        'title':'home',
    }
    return render(request, 'post/index.html', context)

def post(request, slug):
    post = get_object_or_404(Post, slug=slug)


    if post.active == True:

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.post = post
                form.save()


        comments = post.comments.filter(active=True)
        context = {
            'title':post.title,
            'post':post,
            'comments': comments,
        }
        return render(request, 'post/post.html', context)
    else:
        return Http404()
# Post Forms
@login_required(login_url='login')
@allowed_users(allowed_rules=['author', 'ad min'])
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = request.user
            new_form.save()
            form.save_m2m()
            return redirect('post', slug=new_form.slug)

        else:
            messages.error(request, 'The post not save, some thing wrong please try again')


    context = {
        'title':'Create Post',
        'form':form,
    }
    return render(request,'post/post_form.html', context)

@login_required(login_url='login')
def updatePost(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Check if logined user is post author or site admin
    if not same_user(request, post):
        return HttpResponse("you not allowed to be here")
    
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = request.user
            new_form.save()
            form.save_m2m()
            return redirect('post', slug=new_form.slug)

        else:
            messages.warning(request, 'The post not save, some thing wrong please try again')


    context = {
        'title':'update Post',
        'form':form,
    }
    return render(request,'post/post_form.html', context)


@login_required(login_url='login')
def deletePost(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Check if logined user is post author or site admin
    if not same_user(request, post):
        return HttpResponse("you not allowed to be here")


    if request.method == 'POST':
        post.delete()
        messages.warning(request, 'post deleted Successfully')
        return redirect('/')
    
    return render(request, 'post/delete_post.html', {'post':post})

    
def about(request):

    return render(request, 'post/about.html')


def contact(request):

    context = {

    }

    return render(request, 'post/contact.html', context)
