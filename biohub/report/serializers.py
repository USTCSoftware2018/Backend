from rest_framework import serializers
from report.models import Report, Step, SubRoutine, Label


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'title', 'authors', 'introduction', 'label', 'ntime', 'mtime', 'result', 'subroutines')


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ('id', 'user', 'content_json', 'yield_method')


class SubRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRoutine
        fields = ('id', 'user', 'content_json', 'yield_method')
