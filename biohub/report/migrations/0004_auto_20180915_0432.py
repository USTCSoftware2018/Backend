# Generated by Django 2.1 on 2018-09-15 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20180913_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='yield_method',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subroutine',
            name='yield_method',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
