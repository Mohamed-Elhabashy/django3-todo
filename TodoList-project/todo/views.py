from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .foms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def signupuser(request):
    if request.user is not None:
        logout(request)

    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(currenttodo)
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'This User is alerady taken'})

        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Password did not match'})


def home(request):
    return render(request, 'todo/home.html')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect(home)


def loginuser(request):
    if request.user is not None:
        logout(request)

    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodo')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data try again.'})


@login_required
def currenttodo(request):
    todos = Todo.objects.filter(user=request.user, timecomplete__isnull=True)
    return render(request, 'todo/current.html', {'todos': todos})


@login_required
def showcomplete(request):
    todos = Todo.objects.filter(user=request.user, timecomplete__isnull=False).order_by('-timecomplete')
    return render(request, 'todo/showcomplete.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, user=request.user, pk=todo_pk)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'form': form, 'todo': todo})

    form = TodoForm(request.POST, instance=todo)
    form.save()
    return redirect('currenttodo')


@login_required
def todocomplete(request, todo_pk):
    todo = get_object_or_404(Todo, user=request.user, pk=todo_pk)
    if request.method == 'POST':
        todo.timecomplete = timezone.now()
        todo.save()
        return redirect('currenttodo')


@login_required
def tododelete(request, todo_pk):
    todo = get_object_or_404(Todo, user=request.user, pk=todo_pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodo')
