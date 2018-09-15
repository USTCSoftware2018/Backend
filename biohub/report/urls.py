from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import StepViewSet, SubRoutineViewSet, ReportViewSet

router = DefaultRouter()
router.register('step', StepViewSet)
router.register('subroutine', SubRoutineViewSet)
router.register('report', ReportViewSet)

urlpatterns = [
    url('^', include(router.urls))
]
