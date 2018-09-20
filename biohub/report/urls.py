from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StepViewSet, SubRoutineViewSet, ReportViewSet, report_html

router = DefaultRouter()
router.register('step', StepViewSet)
router.register('subroutine', SubRoutineViewSet)
router.register('report', ReportViewSet)

urlpatterns = [
    path('report/<int:id>/html/', report_html),
    url('^', include(router.urls)),
]
