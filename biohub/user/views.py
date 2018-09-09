from django.shortcuts import render
from django.http import HttpResponse
from .models import User

# Create your views here.

def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
