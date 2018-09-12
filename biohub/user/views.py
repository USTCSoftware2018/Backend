from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import User
from .encoders import UserEncoder

# Create your views here.


