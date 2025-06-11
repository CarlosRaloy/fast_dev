from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('users:ping')
        else:
            return render(request, 'users/login.html', {'error': 'El usuario es invalido'})

    return render(request, 'users/login.html')


@login_required
def ping(request):
    response = "PONG (202)"
    return render(request, template_name='base.html', context={'response': response})
