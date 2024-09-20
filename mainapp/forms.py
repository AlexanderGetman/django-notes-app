from django import forms
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from .models import Article, UploadAvatar, Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
import os

class RegForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    def check_password(self):
        user_password1 = self.cleaned_data['password1']
        user_password2 = self.cleaned_data['password2']
        if user_password1 != user_password2:
            raise ValidationError("Passwords do not match")
        if len(user_password1) < 8:
            raise ValidationError("Password should be at least 8 characters long")
        return True

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Content')
    tags = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Input tags separated by comma'}), label='Tags')

    class Meta:
        model = Article
        fields = ['content', 'tags']

class ChangeNameForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class UploadAvatarForm(forms.ModelForm):
    
    class Meta:
        model = UploadAvatar
        fields = ['avatar']