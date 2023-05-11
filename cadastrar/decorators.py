from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse
from rolepermissions.decorators import \
    has_permission_decorator as original_decorator


def has_permission_decorator(permission):
    def decorator(view_func):
        original_decorator_func = original_decorator(permission)(view_func)

        def _wrapped_view(request, *args, **kwargs):
            if request.user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            else:
                # Redireciona para a página inicial se o usuário não tiver a permissão necessária
                return redirect('home')
        return _wrapped_view
    return decorator



