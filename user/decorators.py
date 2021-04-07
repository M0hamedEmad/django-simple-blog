from django.shortcuts import redirect


def unathenticated_user(view_func):
    def wrapper_func(requset, *args, **kwargs):
        if requset.user.is_authenticated:
            return redirect('/')
        
        return view_func(requset, *args, **kwargs)

    return wrapper_func

