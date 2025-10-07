from django.shortcuts import render
from web import models
def admin_list(request):
    """用户列表"""
    #queryset 相当于一个列表，列表中是一个个用户对象
    queryset = models.Admin.objects.all()
    return render(request,"admin.html",{"queryset":queryset})