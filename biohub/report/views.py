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


# Create your views here.


def _merge_id(j, id):
    """
    add/update an 'id' field to a json document
    :param j: a json object
    :param id: id field to be added
    :return: a new json object
    """
    d = json.loads(j)
    d['id'] = id
    return json.dumps(d)


def _assemble(o):
    """
    Assemble a Report object into one json document.
    This object must be a valid object stored in the database.
    :param o: a Report object
    :return: a json document
    """
    d = {
        'id': o.id,
        'title': o.title,
        'introduction': o.introduction,
        'ntime': o.ntime,
        'mtime': o.mtime,
        'result': o.result,
        'subroutines': [],
        'author': []
    }
    for subr in o.subroutines:
        d['subroutines'].append(json.loads(subr))
    for author in o.authors:
        d['author'].append(author.actualname)
    return json.dumps(d)


def login_required(f):
    """
    This differs from the Django version: it reports the error instead of redirecting to login page.
    """
    def _decorated(request, *args, **kwargs):
        user = request.user
        if not user or not user.is_active:
            return JsonResponse({
                'meta': {
                    'success': False,
                    'message': 'Not logged in'
                },
                'data': None
            })
        return f(request, *args, **kwargs)
    return _decorated


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


@require_GET
@login_required
def get_subroutines(request):
    subroutines = SubRoutine.objects.filter(user=request.user)
    reply = {
        'meta': {
            'success': True,
            'message': 'Success'
        },
        'data': {
            'subroutine': [_merge_id(subr.content_json, subr.id) for subr in subroutines]
        }
    }
    return JsonResponse(reply)


@require_GET
@login_required
def get_subroutine(request, id):
    try:
        subr = SubRoutine.objects.get(id=id)
        if subr.user != request.user:
            return JsonResponse({
                'meta': {
                    'success': False,
                    'message': 'Bug: This step does not belong to this user'
                },
                'data': []
            })
        return JsonResponse({
            'meta': {
                'success': True,
                'message': 'Success'
            },
            'data': {
                'subroutine': _merge_id(subr.content_json, subr.id)
            }
        })
    except SubRoutine.DoesNotExist:
        return Http404()


@require_GET
@login_required
def get_steps(request):
    steps = Step.objects.filter(user=request.user)
    reply = {
        'meta': {
            'success': True,
            'message': 'Success'
        },
        'data': {
            'step': [_merge_id(step.content_json, step.id) for step in steps]
        }
    }
    return JsonResponse(reply)


@require_GET
@login_required
def get_report(request, id):
    try:
        report = Step.objects.get(id=id)
        if request.user not in report.authors:
            return JsonResponse({
                'meta': {
                    'success': False,
                    'message': 'This step does not belong to this user'
                },
                'data': []
            })
        return JsonResponse({
            'meta': {
                'success': True,
                'message': 'Success'
            },
            'data': {
                'report': _assemble(report)
            }
        })
    except Report.DoesNotExist:
        return Http404()


@require_GET
@login_required
def get_reports(request):
    reports = request.user.reports
    return JsonResponse({
        'meta': {
            'success': True,
            'message': 'Success'
        },
        'data': {
            'report': [_assemble(report) for report in reports]
        }
    })


@require_POST
@login_required
def update_step(request):
    content_json = request.POST.body.decode()
    d = json.loads(content_json)
    try:
        o = Step.objects.get(id=d['id'])
        if o.user != request.user:
            return JsonResponse({
                'meta': {
                    'success': False,
                    'message': 'Bug: This step does not belong to this user'
                },
                'data': []
            })
        o.content_json = content_json
    except KeyError:
        o = Step.objects.create(user=request.user, content_json=content_json)
    o.save()
    return JsonResponse({
        'meta': {
            'success': True,
            'message': 'Success'
        },
        'data': {
            'id': o.id
        }
    })


@require_POST
@login_required
def update_subroutine(request):
    content_json = request.POST.body.decode()
    d = json.loads(content_json)
    try:
        o = SubRoutine.objects.get(id=d['id'])
        if o.user != request.user:
            return JsonResponse({
                'meta': {
                    'success': False,
                    'message': 'Bug: This step does not belong to this user.'
                },
                'data': []
            })
        o.content_json = content_json
    except KeyError:
        o = SubRoutine.objects.create(user=request.user, content_json=content_json)
    o.save()
    return JsonResponse({
        'meta': {
            'success': True,
            'message': 'Success'
        },
        'data': {
            'id': o.id
        }
    })


@require_POST
@login_required
def update_report(request):
    full_json = request.POST.body.decode()
    d = json.loads(full_json)
    try:
        o = Report.objects.get(id=d['id'])
        if o.user != request.user:
            return JsonResponse({
                'meta': {
                    'success': False,
                    'message': 'Bug: This step does not belong to this user'
                },
                'data': []
            })
    except KeyError:
        o = Report.objects.create(id=d['id'], user=request.user)
    o.title = d.get('title', 'Untitled')
    o.introduction = d.get('introduction', '')
    o.label = [Label.objects.get_or_create(label_name=label) for label in d.get('label', {})]
    for k in ['ntime', 'mtime']:
        if k in d:
            setattr(o, k, d[k])
    o.result = d.get('result', '')
    o.subroutines = [json.dumps(subr) for subr in d.get('subroutines', {})]
    o.save()
    return JsonResponse({
        'meta': {
            'success': True,
            'message': 'Success'
        },
        'data': {
            'id': o.id
        }
    })


@require_http_methods(['POST', 'GET'])
@login_required
def step(request):
    if request.method == 'POST':
        return get_steps(request)
    elif request.method == 'GET':
        return update_step(request)


@require_http_methods(['POST', 'GET'])
@login_required
def subroutine(request):
    if request.method == 'POST':
        return get_subroutines(request)
    elif request.method == 'GET':
        return update_subroutine(request)


@require_http_methods(['POST', 'GET'])
@login_required
def report(request):
    if request.method == 'POST':
        return get_reports(request)
    elif request.method == 'GET':
        return update_report(request)
