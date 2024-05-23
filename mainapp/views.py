from django.shortcuts import render, redirect, HttpResponse
from .models import User, Note
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegForm, LoginForm
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Create your views here.
def index_page(request):    
    return render(request, 'index.html', {'page': 'index'})

def reg_page(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            try:
                form.check_password()
            except ValidationError as e:
                return render(request, "reg.html", context={'form': form, 'e': e.message})
            
            username = form["username"].value()
            email = form["email"].value()
            first_name = form["first_name"].value()
            last_name = form["last_name"].value()
            password1 = form["password1"].value()

            try:
                newuser = User.create_user(username, first_name, last_name, email, password1)
                return redirect(index_page)
            except IntegrityError as e:
                if 'unique constraint' in e.message:
                    return render(request, "reg.html", context={'form': form, 'e': 'Username or email already exists.'})
                    
    else:
        form = RegForm()
    context = {'form': form}
    return render(request, "reg.html", context)

def login_page(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form["username"].value()
            password = form["password"].value()
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, "login.html", context={'form': form, 'e': 'No user with this username and / or password have been found'})
            login(request, user)
            return redirect(index_page)

def logout_page(request):
    logout(request)
    return render(request, "index.html")

@login_required(login_url='/login/')
def add_note_page(request):
    if request.method == "GET":
        return render(request, 'add_note.html')
    else:
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        note = request.POST.get('note-text')
        Note.objects.create(user=user, text=note)
        return(redirect(add_note_page))

@login_required(login_url='/login/')
def notes_page(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    notes = Note.objects.filter(user=user)
    if request.method == "POST":
        note_id = request.POST.get('id')
        try:
            note = Note.objects.get(id=note_id)
            note.delete()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    return render(request, 'notes.html', {'page': 'notes', 'notes': notes})

@login_required(login_url='/login/')
def account_page(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    number_of_notes = Note.objects.filter(user=user).count()
    return render(request, 'account.html', context={"number_of_notes": number_of_notes})