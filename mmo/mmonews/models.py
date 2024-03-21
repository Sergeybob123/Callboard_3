from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    user = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Заголовок')
    text = models.TextField(default='Текст объявления')
    datetime_post = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'


class Response(models.Model):
    text = models.TextField()
    datetime_response = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text[:20]}...'

    def get_absolute_url(self):
        return f'/response/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)