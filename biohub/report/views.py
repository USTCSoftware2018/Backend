from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.conf import settings
import json
from django.utils import timezone
from .models import Graph, SubRoutine, Step, Report, Label
from user.models import User
from.models import Report, Comment, CommentReply
from django.contrib import auth
from django.core import serializers

from rest_framework.viewsets import ModelViewSet
from .serializers import StepSerializer, SubRoutineSerializer, ReportSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsAuthorOrReadyOnly


class StepViewSet(ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        return Step.objects.filter(user=user)


class SubRoutineViewSet(ModelViewSet):
    queryset = SubRoutine.objects.all()
    serializer_class = SubRoutineSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        return SubRoutine.objects.filter(user=user)


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadyOnly)


def post_picture(request):
    if request.method == 'POST' or 'OPTIONS':
        user_pk = request.user.pk
        user = User.objects.get(pk=user_pk)
        uidb64 = bytes.decode(urlsafe_base64_encode(force_bytes(user.pk)))
        if user and user.is_active:
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
                response = HttpResponse(content_type="application/json")
                response.write(json.dumps(err_msg))
                return response

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
                response = HttpResponse(content_type="application/json")
                response.write(json.dumps(msg))
                return response
                # return HttpResponse(json.dumps(msg))
            else:
                err_msg = {
                    'meta': {
                        'success': False,
                        'message': 'Picture Is Too Large Or Too Small',
                    },
                    'data': str(picture.size/1000) + 'kb'
                }
                response = HttpResponse(content_type="application/json")
                response.write(json.dumps(err_msg))
                return response
        else:
            err_msg = {
                'meta': {
                    'success': False,
                    'message': 'Identify Error',
                },
                'data': None,
            }
            response = HttpResponse(content_type="application/json")
            response.write(json.dumps(err_msg))
            return response
    else:
        err_msg = {
            'meta': {
                'success': False,
                'message': 'Method Error',
            },
            'data': None,
        }
        response = HttpResponse(content_type="application/json")
        response.write(json.dumps(err_msg))
        return response


def comment_post(request):
    if request.method == 'POST':
        comment_json = request.POST.get('comment', '')
        comment = json.loads(comment_json)
        report_pk = comment['to_report']
        report = Report.objects.get(pk=report_pk)
        user = request.user
        message = comment['message']  # message
        to_comment = comment['to_comment']  # comment_pk
        # to_comment = json.loads(to_comment)

        if user is not None and user.is_active:
            # if user.email_status is Trgit ue:
            # auth.login(request, user)

            # user.login_times += 1
            # user.save()

            if to_comment['type'] == 'master':
                new_comment = Comment()
                new_comment.user = user
                new_comment.text = message
                new_comment.to_report = report
                new_comment.save()
            elif to_comment['type'] == 'main':
                new_comment = CommentReply()
                new_comment.user = user
                new_comment.text = message
                new_comment.to_report = report
                new_comment.reply_to = None
                super_comment = Comment.objects.get(id=to_comment['value'])
                new_comment.super_comment = super_comment
                new_comment.save()
            else:
                new_comment = CommentReply()
                new_comment.user = user
                new_comment.text = message
                new_comment.to_report = report
                reply_to = CommentReply.objects.get(id=to_comment['value'])
                super_comment = reply_to.super_comment
                new_comment.reply_to = reply_to
                new_comment.super_comment = super_comment
                new_comment.save()

            # return redirect(reverse("article", kwargs={'slug': slug}))
            # else:
            #     response = {
            #         'email_status': False,
            #     }
            #     return HttpResponse(json.dumps(response), content_type='application/json')
            # else:
            #     # user not active
            #     new_user = User()
            #     new_user.true_name = fullname
            #     new_user.email = email
            #     new_user.website = website
            #     random_pswd = gen_pswd(email)
            #     new_user.password = make_password(random_pswd)
            #     # new_user.email_status = False
            #     new_user.save()
            #
            #     send_confirm_mail(request, new_user, random_pswd)
            #     return redirect(reverse(
            #         'email_send_status',
            #         kwargs={
            #             'uidb64': bytes.decode(urlsafe_base64_encode(force_bytes(new_user.pk))),
            #             'status': 'success',
            #         }
            #     )
            #     )

        else:
            pass
