from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # if user us authenticated, don't let them see specified psge
        # redirect to home page instead
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

# restrict access to function, only allow users in allowed_roles
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('allowed roles: ', allowed_roles)

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else: 
                return HttpResponse('You are not authorized to view this page.')

        return wrapper_func
    return decorator




'''
# if user is logged in and goes to home page, redirect to user home page
def user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_page')
        return view_func(request, *args, **kwargs)
    return wrapper_func
'''