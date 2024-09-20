from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from typing import Iterable

# Create your models here.

class ListField(models.TextField):
    """
    A custom Django field to represent lists as comma separated strings
    """

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['token'] = self.token
        return name, path, args, kwargs

    def to_python(self, value):

        class SubList(list):
            def __init__(self, token, *args):
                self.token = token
                super().__init__(*args)

            def __str__(self):
                return self.token.join(self)

        if isinstance(value, list):
            return value
        if value is None:
            return SubList(self.token)
        return SubList(self.token, value.split(self.token))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if not value:
            return
        assert(isinstance(value, Iterable))
        return self.token.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

class User(AbstractUser):
    @classmethod
    def create_user(cls, username, first_name, last_name, email, password):        
        user = cls.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        return user

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

class Tag(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, null=True)

    def __str__(self):
        return self.content[:50]

def upload_file_path(instance, filename):
    name, ext = filename.split('.')
    file_path = 'images/{account_id}/avatars/{name}.{ext}'.format(account_id=instance.user_id, name=name, ext=ext)
    return file_path

class UploadAvatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=upload_file_path)

    def clean(self):
        super().clean()
        if self.avatar:
            # Check the size of the avatar
            max_size = 3 * 1024 * 1024  # 3 MB
            if self.avatar.size > max_size:
                raise ValidationError(f'Avatar size must be less than {max_size / (1024 * 1024)} MB')