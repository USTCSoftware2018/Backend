from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

import re
from report.models import Report


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
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='following', blank=True)

    reports = models.ManyToManyField(Report, symmetrical=False, related_name='authors')

    collections = models.ManyToManyField(Report, symmetrical=False, related_name='collected_by')

    # report.praises is the persons that praise the report
    favourites = models.ManyToManyField(Report, related_name='praises')

    # first name and last name save
    def save(self, *args, **kwargs):

        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        name = self.actualname
        match = zh_pattern.search(name, 0)

        if match:
            self.last_name = match.group()[0]
            self.first_name = match.group()[1:]
        else:
            name_list = name.split(' ')
            self.first_name = name_list[0]
            self.last_name = name_list[-1]

        super(User, self).save(*args, **kwargs)
