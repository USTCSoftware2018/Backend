# Generated by Django 2.1 on 2018-09-19 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_auto_20180919_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='label',
            field=models.ManyToManyField(related_name='reports_related', to='report.Label'),
        ),
    ]
