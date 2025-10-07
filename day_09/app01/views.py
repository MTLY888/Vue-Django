from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import forms
from django.core.validators import RegexValidator
from app01 import models
class LoginForm(forms.Form):
    user = forms.CharField(label="用户名",
    widget=forms.TextInput(attrs={"class": "form-control","placeholder": "请输入用户名"})
    )
    password = forms.CharField(label="密码",
    widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "请输入密码"},render_value=True) 
    )
class RoleForm(forms.Form):
    user = forms.CharField(label="用户名",
    widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(label="密码",
    widget=forms.PasswordInput(attrs={"class": "form-control"},render_value=True) 
    )
    email = forms.EmailField(label="邮箱",
    widget=forms.EmailInput(attrs={"class": "form-control"}),
    validators=[RegexValidator(r"^[a-z0-9]+@[a-z0-9]+\.[a-z]{2,}$","请输入正确的邮箱")]
    )
# Create your views here.
def add_role(request):
    if request.method == "GET":
        form = RoleForm(initial={"user": "admin","password": "123456","email": "admin@163.com"})
        return render(request, "add_role.html", {"form": form})
    else:
        # 处理POST请求,对用户提交的数据进行校验
        form = RoleForm(request.POST)
        if form.is_valid():
            return HttpResponse("提交成功")
            data = form.cleaned_data   #返回的是字典类型的数据
        else:
            #form.errors 是个对象，包含了所有的错误信息
            #form对象
            return render(request, "add_role.html", {"form": form})

def login(request):  
    #用户登录
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html",{"form": form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            #得到的是字典信息
            data = form.cleaned_data
            # user = models.UserInfo.objects.filter(user=data["user"],password=data["password"]).first()
            user = models.UserInfo.objects.filter(**data).first()   #**data是解包，将字典中的键值对解包成关键字参数
            if user:
                return HttpResponse("登录成功")
            else:
                 return render(request, "login.html", {"form": form,"error_msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"form": form})
def depart_list(request):
    #取部门列表
    queryset = models.Department.objects.all()
    # 计算总人数
    total_count = sum(dept.count for dept in queryset)
    return render(request, "depart_list.html", {
        "queryset": queryset,
        "total_count": total_count
    })
class DepartModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ["title","count"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入部门名称"}),
            "count": forms.NumberInput(attrs={"class": "form-control", "placeholder": "请输入部门人数", "min": "0"})
        }
def add_depart(request):
    if request.method == "GET":
        form = DepartModelForm()
        return render(request, "depart_form.html", {"form": form})
    else:
        form = DepartModelForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect("/depart/list/")
        else:
            return render(request, "depart_form.html", {"form": form})
def delete_depart(request):
    did = request.GET.get("did")
    if did:
        try:
            # 确保did是整数
            did = int(did)
            models.Department.objects.filter(id=did).delete()
        except (ValueError, TypeError):
            # 如果转换失败，忽略删除操作
            pass
    return redirect("/depart/list/")

def edit_depart(request):
    did = request.GET.get("did")
    if not did:
        return redirect("/depart/list/")
    
    try:
        did = int(did)
        depart_obj = models.Department.objects.filter(id=did).first()
        if not depart_obj:
            return redirect("/depart/list/")
    except (ValueError, TypeError):
        return redirect("/depart/list/")
    
    if request.method == "GET":
        form = DepartModelForm(instance=depart_obj)
        return render(request, "depart_form.html", {"form": form})
    else:
        form = DepartModelForm(data=request.POST, instance=depart_obj)
        if form.is_valid():
            form.save()
            return redirect("/depart/list/")
        else:
            return render(request, "depart_form.html", {"form": form})
