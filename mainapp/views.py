from django.shortcuts import render, redirect, HttpResponse
from .models import User, Note, Article, UploadAvatar
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegForm, LoginForm, ArticleForm, ChangeNameForm, UploadAvatarForm
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

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
    form = ArticleForm(request.POST)
    if request.method == "GET":
        return render(request, 'add_note.html', context={'article_form': form})
    else:        
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if form.is_valid():
            article_text = request.POST.get('content', '')
            article = form.save(commit=False)
            article.content = article_text
            article.user = user
            article.save()
            return redirect(add_note_page)
        return(redirect(add_note_page))

@login_required(login_url='/login/')
def notes_page(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    articles = Article.objects.filter(user=user)
    if request.method == "POST":
        article_id = request.POST.get('id')
        try:
            article = Article.objects.get(id=article_id)
            article.delete()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    return render(request, 'notes.html', {'page': 'notes', 'articles': articles})

@login_required(login_url='/login/')
def account_page(request):    
    user = request.user
    number_of_notes = Article.objects.filter(user=user).count()

    form = PasswordChangeForm(user=user)
    change_avatar_form = UploadAvatarForm()
    change_name_form = ChangeNameForm()

    if request.method == "POST":
        if 'change_password' in request.POST:
            form = PasswordChangeForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('/')
        elif "change_avatar" in request.POST:
            change_avatar_form = UploadAvatarForm(request.POST, request.FILES)
            if change_avatar_form.is_valid():
                UploadAvatar.objects.filter(user=user).delete()
                avatar_instance = change_avatar_form.save(commit=False)
                avatar_instance.user = user
                avatar_instance.save()
                return redirect('/')
        elif 'change_name' in request.POST:
            change_name_form = ChangeNameForm(request.POST)
            if change_name_form.is_valid() and user.check_password(change_name_form.cleaned_data["password"]):            
                user.first_name = change_name_form.cleaned_data["first_name"]
                user.last_name = change_name_form.cleaned_data["last_name"]
                user.save()
                return redirect('/')

    return render(request, 'account.html', context={
        "number_of_notes": number_of_notes,
        "form": form,
        "change_name_form": change_name_form,
        "change_avatar_form": change_avatar_form
    })
