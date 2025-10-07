# evaluation_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),  # 认证相关的API
    path('api/', include('evaluation.urls')),  # 评估相关的API
]