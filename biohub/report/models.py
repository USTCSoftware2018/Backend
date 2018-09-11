from django.db import models
from django.conf import settings
# Create your models here.


class Report(models.Model):

    title = models.CharField(max_length=256)
    abstract = models.TextField()
    labels = models.ManyToManyField('Label', related_name='reports_related')
    pub_time = models.DateTimeField(auto_now_add=True)
    latest_edit_time = models.DateTimeField(auto_now=True)
    # See comments in Comment model!
    # See praises(likes in the doc) in User model

    def __str__(self):
        return 'id:{}, title:{}'.format(self.pk, self.id)


class Label(models.Model):
    label_name = models.CharField(max_length=64)

    def __str__(self):
        return 'id:{}, name:{}'.format(self.pk, self.label_name)


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


# Edit process
class Component(models.Model):
    icon = models.URLField()
    name = models.CharField(max_length=64)
    description = models.TextField()
    template = models.TextField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collected_steps')
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_steps', on_delete=models.CASCADE)

    def __str__(self):
        return 'id:{}, name: {}'.format(self.pk, self.name)


class SubRoutine(models.Model):
    icon = models.URLField()
    name = models.CharField(max_length=64)
    description = models.TextField()
    default = models.TextField()
    data = models.ManyToManyField(Component, through='SubroutingComponent')

    def data_list(self):
        return [sc.component for sc in SubroutingComponent.objects.filter(sub_routine=self).order_by('order')]

    def __str__(self):
        return 'id:{}, name:{}'.format(self.pk, self.name)


class SubroutingComponent(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    sub_routine = models.ForeignKey(SubRoutine, on_delete=models.CASCADE, db_index=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return 'comp:{}, subr:{}, no:{}'.format(self.component.name, self.sub_routine.name, self.order)
