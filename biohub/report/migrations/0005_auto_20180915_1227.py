# Generated by Django 2.1 on 2018-09-15 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_auto_20180915_0432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='label_name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]