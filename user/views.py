from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import UserForm, ProfileEditForm, ProfileForm
from post.models import Post
from .decorators import unathenticated_user

@unathenticated_user
def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
        else:
            messages.warning(request, "Something's wrong. Please check again")

    context = {
        'title':'register',
        'form':form,
    }

    return render(request, 'user/register.html', context)

@unathenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')
        
        else:
            messages.warning(request, "username or password are wrong")

    context = {
        'title':'login',
    }

    return render(request, 'user/login.html', context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    posts = request.user.post.filter(active=True)

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context = {
        'title':request.user.username,
        'posts':posts,
    }
    return render(request, 'user/profile.html', context)

@login_required(login_url='login')
def profile_edit(request):

    # show a user form
    form = ProfileEditForm(instance=request.user)

    if request.method == 'POST':
        
        # Verify that the password entered by the user is correct
        password_confirm = request.POST.get('password_confirm')
        user_password = request.user.check_password(password_confirm)

        # if password True
        if user_password:
            form = ProfileEditForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if form.is_valid() and profile_form.is_valid():
                form.save()
                profile_form.save()
                return redirect('profile')

            else:
                messages.warning(request, 'The profile not save, some thing wrong please try again')
        
        # if password False
        else:
            messages.warning(request, 'password is wrong please try again')


    context = {
        'title':'update Post',
        'form':form,
    }
    return render(request,'user/edit_profile.html', context)