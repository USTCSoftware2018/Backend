# Generated by Django 2.1 on 2018-09-12 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.URLField()),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('template', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ComponentJson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graph', models.ImageField(blank=True, null=True, upload_to='report_graph')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('abstract', models.TextField()),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('latest_edit_time', models.DateTimeField(auto_now=True)),
                ('templates', models.TextField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SubRoutine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rt_type', models.CharField(choices=[('ST', 'Steps'), ('IN', 'Info'), ('RE', 'Result'), ('PI', 'Pictures'), ('QU', 'Quote'), ('TE', 'Text'), ('TA', 'Table')], max_length=2)),
                ('content_json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SubRoutineJson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_json', models.TextField()),
                ('components', models.ManyToManyField(related_name='subroutines', to='report.ComponentJson')),
            ],
        ),
        migrations.CreateModel(
            name='SubroutingComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component_default_json', models.TextField()),
                ('order', models.IntegerField()),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.Component')),
                ('sub_routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.SubRoutine')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='report.Comment')),
            ],
            bases=('report.comment',),
        ),
    ]
