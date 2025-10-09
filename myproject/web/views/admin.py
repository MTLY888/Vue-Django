from django.shortcuts import render,redirect,HttpResponse
from web import models
from django import forms
from utils.encrypt import md5
from django.http import JsonResponse
def admin_list(request):
    """用户列表"""
    #queryset 相当于一个列表，列表中是一个个用户对象
    queryset = models.Admin.objects.all()
    return render(request,"admin.html",{"queryset":queryset})
class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username","password","gender","depart"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing_class + " form-control").strip()
            field.widget.attrs.setdefault("placeholder", field.label)

class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username","gender","depart"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing_class + " form-control").strip()
            field.widget.attrs.setdefault("placeholder", field.label)

def admin_add(request):
    """新建用户"""
    if request.method=="GET":
        form = AdminModelForm()
        return render(request,"admin_form.html",{"form":form})
    else:
        form = AdminModelForm(request.POST)
        if form.is_valid():
            form.instance.password = md5(form.instance.password)
            form.save()
            return redirect("/admin/list/")
        else:
            return render(request,"admin_form.html",{"form":form})

def admin_edit(request,aid):
    obj = models.Admin.objects.filter(id=aid).first()
    if request.method=="GET":
        form = AdminEditModelForm(instance=obj)
        return render(request,"admin_form.html",{"form":form})
    else:
        form = AdminEditModelForm(instance=obj,data=request.POST) 
        """如果不带instance参数，则会创建一个新的对象，如果带了instance参数，则会更新这个对象"""
        if form.is_valid():
            form.instance.password = md5(form.instance.password)
            form.save()
            return redirect("/admin/list/")

def admin_delete(request):
    aid = request.GET.get("aid")
    models.Admin.objects.filter(id=aid).delete()
    # return JsonResponse({"status":False,"error":"相应的错误反馈信息"})
    return JsonResponse({"status":True})
    