from django.shortcuts import render
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.conf import settings
import json
from django.utils import timezone
from .models import Graph
from user.models import User

# Create your views here.


def post_picture(request):
    if request.method == 'POST' or 'OPTIONS':
        user = User.objects.filter(pk=1)[0]
        uidb64 = bytes.decode(urlsafe_base64_encode(force_bytes(user.pk)))
        # if user and user.is_active:
        try:
            picture = request.FILES.get('file')
        except:
            err_msg = {
                'meta': {
                    'success': False,
                    'message': 'No Picture Updated',
                },
                'data': None
            }
            respone = HttpResponse(content_type="application/json")
            respone.write(json.dumps(err_msg))
            return respone

        if 10000 < picture.size < 409600000:
            picture.name = uidb64 + '_' + timezone.now().strftime('%Y%m%d%H%M%S') + '_' + picture.name
            image = Graph(owner=user, graph=picture)
            image.save()
            msg = {
                'meta': {
                    'success': True,
                    'message': 'Success',
                },
                'data': settings.MEDIA_ROOT + image.graph.url
            }
            respone = HttpResponse(content_type="application/json")
            respone.write(json.dumps(msg))
            return respone
            # return HttpResponse(json.dumps(msg))
        else:
            err_msg = {
                'meta': {
                    'success': False,
                    'message': 'Picture Is Too Large Or Too Small',
                },
                'data': str(picture.size/1000) + 'kb'
            }
            respone = HttpResponse(content_type="application/json")
            respone.write(json.dumps(err_msg))
            return respone
        # else:
        #     err_msg = {
        #         'meta': {
        #             'success': False,
        #             'message': 'Identify Error',
        #         },
        #         'data': None,
        #     }
        #     respone = HttpResponse(content_type="application/json")
        #     respone.write(json.dumps(err_msg))
        #     return respone
    else:
        err_msg = {
            'meta': {
                'success': False,
                'message': 'Method Error',
            },
            'data': None,
        }
        respone = HttpResponse(content_type="application/json")
        respone.write(json.dumps(err_msg))
        return respone


