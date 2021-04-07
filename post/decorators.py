from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_rules=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            elif request.user.groups.exists():
                groups = request.user.groups.all()

                for group in groups:
                    if group.name in allowed_rules:
                        return view_func(request, *args, **kwargs)

            
            else:
                return HttpResponse('You Not allowed to visit there url')

        return wrapper_func
    return decorator


def unathenticated_user(view_func):
    def wrapper_func(requset, *args, **kwargs):
        if requset.user.is_authenticated:
            return redirect('/')
        
        return view_func(requset, *args, **kwargs)

    return wrapper_func