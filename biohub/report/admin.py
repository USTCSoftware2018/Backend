from django.contrib import admin
from report.models import Report, Step, SubRoutine, Label

# Register your models here.
admin.site.register(Report)
admin.site.register(Step)
admin.site.register(SubRoutine)
admin.site.register(Label)
