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

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"请输入用户名"})
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"请输入密码"})
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"请再次输入密码"})
    )
def login(request):
    """用户登录"""
    if request.method == "GET":
        form = LoginForm()
        success_message = ""
        error_message = ""
        
        if request.GET.get('success') == '1':
            success_message = "注册成功！请使用新账号登录。"
        elif request.GET.get('deleted') == '1':
            success_message = "账号已成功注销！"
        elif request.GET.get('error') == '1':
            error_message = "操作失败，请重试。"
            
        return render(request,"login.html",{
            "form":form, 
            "success_message": success_message,
            "error_message": error_message
        })
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request,"login.html",{"form":form})
        #判断验证码是否正确
        img_code = request.session.get('captcha_code')
        captcha_time = request.session.get('captcha_time')
        
        if not img_code or not captcha_time:
            form.add_error("code","验证码已经过期，请刷新验证码")
            # 清除可能存在的过期验证码
            request.session.pop('captcha_code', None)
            request.session.pop('captcha_time', None)
            return render(request,"login.html",{"form":form})
        
        # 检查验证码是否过期（60秒）
        import time
        if time.time() - captcha_time > 60:
            form.add_error("code","验证码已经过期，请刷新验证码")
            # 清除过期的验证码
            request.session.pop('captcha_code', None)
            request.session.pop('captcha_time', None)
            return render(request,"login.html",{"form":form})
        
        if img_code.upper() != form.cleaned_data['code'].upper():
            form.add_error("code","验证码错误")
            # 验证码错误后清除session中的验证码，强制用户重新获取
            request.session.pop('captcha_code', None)
            request.session.pop('captcha_time', None)
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
    
    # 将验证码和时间戳存储到session中，用于后续验证
    import time
    request.session['captcha_code'] = code
    request.session['captcha_time'] = time.time()  # 记录验证码生成时间
    
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

def register(request):
    """用户注册"""
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {"form": form})
    else:
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "register.html", {"form": form})
        
        # 获取表单数据
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        
        # 验证两次密码是否一致
        if password != confirm_password:
            form.add_error("confirm_password", "两次输入的密码不一致")
            return render(request, "register.html", {"form": form})
        
        # 检查用户名是否已存在
        if models.Admin.objects.filter(username=username).exists():
            form.add_error("username", "用户名已存在，请选择其他用户名")
            return render(request, "register.html", {"form": form})
        
        # 创建默认部门（如果不存在）
        default_dept, created = models.Department.objects.get_or_create(
            title='默认部门',
            defaults={'title': '默认部门'}
        )
        
        # 创建新用户
        try:
            new_admin = models.Admin.objects.create(
                username=username,
                password=password,  # 这里直接存储明文密码，你也可以使用md5加密
                gender=1,  # 默认性别为男
                depart=default_dept
            )
            
            # 注册成功，跳转到登录页面
            return redirect("/login/?success=1")
        except Exception as e:
            form.add_error("username", f"注册失败：{str(e)}")
            return render(request, "register.html", {"form": form})

def delete_account(request):
    """删除账号"""
    if request.method == "GET":
        # 获取当前登录用户信息
        user_info = request.session.get('userInfo')
        if not user_info:
            return redirect("/login/")
        
        try:
            # 获取用户对象
            user_id = user_info.get('id')
            user = models.Admin.objects.get(id=user_id)
            
            # 删除用户
            user.delete()
            
            # 清除session
            request.session.flush()
            
            # 跳转到登录页面，显示删除成功信息
            return redirect("/login/?deleted=1")
            
        except models.Admin.DoesNotExist:
            # 用户不存在，清除session并跳转
            request.session.flush()
            return redirect("/login/?error=1")
        except Exception as e:
            # 删除失败，跳转到登录页面
            request.session.flush()
            return redirect("/login/?error=1")