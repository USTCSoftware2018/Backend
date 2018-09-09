from django.core.serializers.json import DjangoJSONEncoder


class UserEncoder(DjangoJSONEncoder):
    def default(self, obj):
        return super().default(obj)
