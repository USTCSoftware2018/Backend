from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import User
from .encoders import UserEncoder

# Create your views here.


def get_users(request, id):
    if request.method == 'GET':
        user = User.objects.filter(pk=id)
        users_json = serialize('json', users, cls=UserEncoder)
        # print(users_json)
        respone = HttpResponse(content_type="application/json")
        respone['Access-Control-Allow-Origin'] = '*'
        respone['Access-Control-Allow-Methods'] = 'POST, PUT, DELETE, OPTIONS'
        respone['Access-Control-Allow-Headers'] = 'x-requested-with'
        respone.write(users_json)
        return respone
    # elif request.method == 'DELETE':
    #     pass
    else:
        pass

