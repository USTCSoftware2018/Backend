# Generated by Django 2.1 on 2018-09-19 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_report_envs'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
