"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from web.views import account,admin
urlpatterns = [
    # path("admin/", admin.site.urls),
    path("login/",account.login),
    path("register/",account.register),
    path("img/code/",account.img_code),
    path("home/",account.home),
    path("logout/",account.logout),
    path("delete_account/",account.delete_account),
    path("admin/list/",admin.admin_list),
    path("admin/add/",admin.admin_add),
    # 地址需要为 /admin/edit/123/ 这样我们才能传递aid参数
    path("admin/edit/<int:aid>/",admin.admin_edit),
    # 地址需要为 /admin/delete/?aid=123 这样我们才能传递aid参数
    path("admin/delete/",admin.admin_delete),
]
