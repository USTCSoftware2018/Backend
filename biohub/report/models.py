from django.db import models
from django.conf import settings
import json
from django.http import HttpResponse
# from django.contrib.auth.models import AnonymousUser
# Create your models here.


class Report(models.Model):

    title = models.CharField(max_length=256)
    abstract = models.TextField()
    labels = models.ManyToManyField('Label', related_name='reports_related')
    pub_time = models.DateTimeField(auto_now_add=True)
    latest_edit_time = models.DateTimeField(auto_now=True)
    subrouting_json = models.ManyToManyField('SubRoutineJson')

    # See comments in Comment model!
    # See praises(likes in the doc) in User model

    def __str__(self):
        return 'id:{}, title:{}'.format(self.pk, self.id)


class Label(models.Model):
    label_name = models.CharField(max_length=64)

    def __str__(self):
        return 'id:{}, name:{}'.format(self.pk, self.label_name)


class Graph(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='report_graphs')
    graph = models.ImageField(upload_to='report_graph', null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now=True)
    to_report = models.ForeignKey(Report, on_delete=models.CASCADE, db_index=True, related_name='comments')

    @property
    def all_sub_comments(self):
        return self.sub_comments.all().order_by('time')

    def __str__(self):
        return '{}, {}'.format(self.user, self.text)


class CommentReply(Comment):
    reply_to = models.OneToOneField('self', on_delete=models.CASCADE, default=None, blank=True, null=True,
                                    related_name='replied_by')
    super_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                      related_name='sub_comments')


#####################################################################################################################
# Without using json
# Edit process
class Component(models.Model):
    icon = models.URLField()
    name = models.CharField(max_length=64)
    description = models.TextField()
    template = models.TextField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collected_steps')
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_steps', on_delete=models.CASCADE)
    default = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return 'id:{}, name: {}'.format(self.pk, self.name)


class SubRoutine(models.Model):
    STEP = 'ST'
    INFO = 'IN'
    RESULT = 'RE'
    PICTURES = 'PI'
    QUOTE = 'QU'
    TEXT = 'TE'
    TABLE = 'TA'
    rt_type_choices = (
        (STEP, 'Steps'),
        (INFO, 'Info'),
        (RESULT, 'Result'),
        (PICTURES, 'Pictures'),
        (QUOTE, 'Quote'),
        (TEXT, 'Text'),
        (TABLE, 'Table'),
    )
    rt_type = models.CharField(max_length=2, choices=rt_type_choices, null=False, blank=False)
    main_subuoutine = models.ManyToManyField('MainSubRoutine')
    result_subroutine = models.ManyToManyField('ResultSubRoutine')
    #########################


class BaseSubRoutine(models.Model):
    step_num = models.IntegerField()
    icon = models.URLField()
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return 'id:{}, name:{}'.format(self.pk, self.name)


# MainSubRoutine
class MainSubRoutine(BaseSubRoutine):
    data = models.ManyToManyField(Component, through='SubroutingComponent')

    def data_list(self):
        return [sc.component for sc in SubroutingComponent.objects.filter(sub_routine=self).order_by('order')]


class SubroutingComponent(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    sub_routine = models.ForeignKey(MainSubRoutine, on_delete=models.CASCADE, db_index=True)
    component_default_json = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return 'comp:{}, subr:{}, no:{}'.format(self.component.name, self.sub_routine.name, self.order)


# ResultSubRoutine
class ResultSubRoutine(BaseSubRoutine):
    Result = models.TextField()


###########################################################################################################
# Using json
class SubRoutineJson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subroutings', on_delete=models.CASCADE)
    content_json = models.TextField()
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        try:
            subroutine = json.loads(self.content_json)

            if subroutine.idx:
                self.order = subroutine.idx
            else:
                err_msg = {
                    'meta': {
                        'success': False,
                        'message': 'Idx Does Not Exist',
                    },
                    'data': self.content_json
                }
                return HttpResponse(json.dumps(err_msg))

            return super(SubRoutineJson, self).save(*args, **kwargs)

        except json.decoder.JSONDecodeError:
            err_msg = {
                'meta': {
                    'success': False,
                    'message': 'Json Decode Error',
                },
                'data': self.content_json
            }
            return HttpResponse(json.dumps(err_msg))


class ComponentJson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='steps', on_delete=models.CASCADE)
    content_json = models.TextField()
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        try:
            component = json.loads(self.content_json)
            if component.order:
                self.order = component.idx  # order单独存储
            else:
                err_msg = {
                    'meta': {
                        'success': False,
                        'message': 'Idx Does Not Exist',
                    },
                    'data': self.content_json
                }
                return HttpResponse(json.dumps(err_msg))

            return super(ComponentJson, self).save(*args, **kwargs)

        except json.decoder.JSONDecodeError:
            err_msg = {
                'meta': {
                    'success': False,
                    'message': 'Json Decode Error',
                },
                'data': self.content_json
            }
            return HttpResponse(json.dumps(err_msg))

