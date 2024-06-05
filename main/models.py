from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=False)
    balance = models.IntegerField(default=0, blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = 'User'


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField(max_length=2500, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    creator = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    buy_user = models.ManyToManyField(User, related_name='buy_user')
    owner_user = models.ForeignKey(User, related_name='owner_user', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.CharField(max_length=2500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
