from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError

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