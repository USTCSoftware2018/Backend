"""biohub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
import user.views as user_views
import report.views as report_views

router = DefaultRouter()

# different apps' urls separate with space.
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),

    # user's routing
    # path('users/<int:id>/', user_views.get_users, name='get_users'),

    # report's routing
    # FIXME: this should merge with /api router.
    path('editor/pic/', report_views.post_picture, name='post_picture'),
    url(r'^editor/', include('report.urls'))
]

# 部署的时候需要指定static_url 和 media_url
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
