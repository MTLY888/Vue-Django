from django.shortcuts import render,redirect
from app01 import models
# Create your views here.
def login(request):
    if request.method == "GET":
        # GET请求：显示登录页面
        return render(request, "login.html")
    
    # POST请求：处理登录逻辑
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    # 判断用户名和密码是否正确
    user_object = models.UserInfo.objects.filter(username=username, password=password).first() 
    if user_object:
        # 登录成功：设置session并跳转到home页面
        request.session["info"] = user_object.username
        return redirect("/home/")
    else:
        # 登录失败：显示错误信息
        return render(request, "login.html", {"error_msg": "用户名或密码错误"})
def home(request):
    #判断用户是否已经登陆，未登录则跳转到登陆页面
    info = request.info
    return render(request, "home.html",{"info":info})