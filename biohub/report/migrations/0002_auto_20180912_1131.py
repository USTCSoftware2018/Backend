# Generated by Django 2.1 on 2018-09-12 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('report', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subroutinejson',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subroutings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='report',
            name='labels',
            field=models.ManyToManyField(related_name='reports_related', to='report.Label'),
        ),
        migrations.AddField(
            model_name='report',
            name='subrouting_json',
            field=models.ManyToManyField(to='report.SubRoutineJson'),
        ),
        migrations.AddField(
            model_name='graph',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_graphs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='componentjson',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='component',
            name='created_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_steps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='component',
            name='users',
            field=models.ManyToManyField(related_name='collected_steps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='to_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='report.Report'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subroutingcomponent',
            name='sub_routine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.MainSubRoutine'),
        ),
        migrations.AddField(
            model_name='subroutine',
            name='main_subuoutine',
            field=models.ManyToManyField(to='report.MainSubRoutine'),
        ),
        migrations.AddField(
            model_name='subroutine',
            name='result_subroutine',
            field=models.ManyToManyField(to='report.ResultSubRoutine'),
        ),
        migrations.AddField(
            model_name='mainsubroutine',
            name='data',
            field=models.ManyToManyField(through='report.SubroutingComponent', to='report.Component'),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='reply_to',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replied_by', to='report.CommentReply'),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='super_comment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_comments', to='report.Comment'),
        ),
    ]
