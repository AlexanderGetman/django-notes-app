from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

# Create your models here.
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

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()