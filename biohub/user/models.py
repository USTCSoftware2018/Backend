from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


# User main model
class User(AbstractUser):
    # id is auto incresing, use User.pk instead
    actualname = models.CharField(max_length=30, default="Anonymous User")

    location = models.CharField(max_length=256, default='')

    organization = models.CharField(max_length=256, default='')

    # 'img' in interface doc
    portrait = models.ImageField(upload_to='portraits', null=True, blank=True)

    # 'about_me' in interface doc
    profile = models.TextField()

    # being followed by
    # find following persons, use Alice.following.all()
    # find followers, use Bob.followers.all()
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='following', null=True,
                                       blank=True)

    # being praised by
    praises = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='favourites')

    reports = models.ManyToManyField('report', symmetrical=False, related_name='authors')

    collections = models.ManyToManyField('report', symmetrical=False, related_name='collected_by')


