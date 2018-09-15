from rest_framework import serializers
from report.models import Report, Step, SubRoutine, Label
from user.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    """
    This is a custom SlugRelatedField that automatically create a field instead of
    signalling an error.
    """
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class ReportSerializer(serializers.ModelSerializer):
    authors = serializers.SlugRelatedField(allow_empty=False, many=True, slug_field='username',
                                           queryset=User.objects.all())
    label = CreatableSlugRelatedField(allow_empty=True, many=True, slug_field='label_name',
                                      queryset=Label.objects.all())

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
