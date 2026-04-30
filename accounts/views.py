from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request):
    """Vista de inicio de sesión"""
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('core:inicio')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {username}!')
                # Redirigir a la página que intentaba acceder o al dashboard
                next_url = request.GET.get('next', 'core:inicio')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('accounts:login')