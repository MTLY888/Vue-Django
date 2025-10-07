from io import BytesIO
from django import forms
from django.http import HttpResponse
from django.shortcuts import render,redirect
from web import models
from utils.encrypt import md5
from utils.helper import generate_captcha
class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"请输入用户名"})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"请输入密码"},render_value=True)
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"请输入验证码"})
    )
def login(request):
    """用户登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request,"login.html",{"form":form})
        #判断验证码是否正确
        img_code = request.session.get('captcha_code')
        if not img_code:
            form.add_error("code","验证码已经过期，请刷新验证码")
            # 清除可能存在的过期验证码
            request.session.pop('captcha_code', None)
            return render(request,"login.html",{"form":form})
        if img_code.upper() != form.cleaned_data['code'].upper():
            form.add_error("code","验证码错误")
            # 验证码错误后清除session中的验证码，强制用户重新获取
            request.session.pop('captcha_code', None)
            return render(request,"login.html",{"form":form})
        #判断用户名和密码是否正确
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # encrypted_password = md5(password)
        admin = models.Admin.objects.filter(username=username,password=password).first()
        if not admin:
            form.add_error("username","用户名或密码错误")
            return render(request,"login.html",{"form":form})
        #登录成功
        request.session['userInfo'] = {
            "id":admin.id,
            "name":admin.username
        }
        return redirect("/home/")

def img_code(request):
    """生成验证码"""
    img_base64, code = generate_captcha()
    
    # 将验证码存储到session中，用于后续验证
    request.session['captcha_code'] = code
    #设置超时时间
    request.session.set_expiry(60)
    
    # 解码base64字符串为图片数据
    import base64
    img_data = base64.b64decode(img_base64)
    
    # 返回图片响应
    response = HttpResponse(img_data, content_type='image/png')
    return response

def home(request):
    """首页"""
    return render(request,"home.html")

def logout(request):
    """退出登录"""
    request.session.flush()  # 清除所有session数据 
    return redirect("/login/")