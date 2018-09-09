from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import User
from .encoders import UserEncoder

# Create your views here.


def get_users(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            users = User.objects.all()
            users_json = serialize('json', users, cls=UserEncoder)
            # print(users_json)
            respone = HttpResponse(content_type="application/json")
            respone['Access-Control-Allow-Origin'] = '*'
            respone['Access-Control-Allow-Methods'] = 'POST, PUT, DELETE, OPTIONS'
            respone['Access-Control-Allow-Headers'] = 'x-requested-with'
            respone.write(users_json)
            return respone
        elif request.method == 'POST':
            pass
        else:
            pass
    else:
        pass


