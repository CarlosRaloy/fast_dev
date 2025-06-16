from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from aplications.users.forms import SignupForm, ProfileForm
from django.urls import reverse
from .models import Profile

def login_view(request):
    registrado = request.GET.get('registrado') == '1'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('users:ping')
        else:
            return render(request, 'users/login.html', {
                'error': 'El usuario o la contraseña son inválidos',
                'registrado': registrado
            })

    # GET
    return render(request, 'users/login.html', {
        'registrado': registrado
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # redirigimos con ?registrado=1
            return redirect(f"{reverse('users:login')}?registrado=1")
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {
        'form': form
    })



@login_required
def update_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            profile.picture = data['picture']
            profile.theme = data['theme']
            profile.save()

            return redirect('users:ping')
    else:
        form = ProfileForm()
    return render(
        request=request,
        template_name='users/update_profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form
        }
    )


@login_required
def ping(request):
    return render(request, 'blank.html', {'response': 'PONG (200)'})
