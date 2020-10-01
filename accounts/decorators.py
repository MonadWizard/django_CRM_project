from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func




def allowed_user(allowed_rools=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_rools:
                return view_func(request, *args, **kwargs)
            
            else:
                return HttpResponse('Sorry! you are not allowed')
    
        return wrapper_func
    return decorator


# every time any user route to our / url so, for customer we need to fix it by same as allowed_user()'s decorator()



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':
            return redirect('user-page')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func
