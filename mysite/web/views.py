from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from web import models
def login(request): 
    #判断到底是post还是get请求
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        #去请求体中获取数据，再进行校验   {获取前端的user,pwd}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'cheng' and pwd == '123456':
            return redirect('/index/')
        else:
            # 验证失败时，返回登录页面并提示错误（可选）
            return render(request, 'login.html', {'error': '账号或密码错误'})
# Create your views here.
def user_list(request):
    data = ['chengxu','xiaohe','xiaohong']
    return render(request, 'user_list.html',{'message':"这个是网页的标题",'data_list':data})
def phone_list(request):
    return render(request, 'phone_list.html',{'phone_list':queryset})
def index(request):
    #数据库获取数据进行展示和渲染
    queryset = [
        {'id':1,'phone': '13800138000','city' :'上海'},
        {'id':2,'phone': '13800138001','city' :'北京'},
        {'id':3,'phone': '13800138002','city' :'广州'},
        {'id':4,'phone': '13800138003','city' :'深圳'},
    ]
    return render(request, 'index.html',{'queryset':queryset})
def depart(request):
    #ORM操作
    queryset = models.Department.objects.all()
    return render(request, 'depart.html',{'queryset':queryset})

def add_depart(request): 
    #显示添加部门的页面
    if request.method == 'GET':
        return render(request, 'add_depart.html')
    title = request.POST.get('title')
    count = request.POST.get('count')
    models.Department.objects.create(title=title,count=count)
    return redirect('/depart/')
 
def delete_depart(request):
    id = request.GET.get('id')
    models.Department.objects.filter(id=id).delete()
    return redirect('/depart/')
def edit_depart(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if not id:
            return redirect('/depart/')
            
        depart_object = models.Department.objects.filter(id=id).first()
        if not depart_object:
            return redirect('/depart/')
            
        return render(request, 'edit_depart.html', {'depart_object': depart_object})
    else:
        # 编辑并提交数据
        depart_id = request.POST.get('id')
        title = request.POST.get('title')
        count = request.POST.get('count')
        
        if not depart_id:
            return redirect('/depart/')
        
        # 数据验证
        if not title or not title.strip():
            depart_object = models.Department.objects.filter(id=depart_id).first()
            return render(request, 'edit_depart.html', {
                'depart_object': depart_object,
                'error': '部门名称不能为空'
            })
        
        if not count or not count.strip():
            depart_object = models.Department.objects.filter(id=depart_id).first()
            return render(request, 'edit_depart.html', {
                'depart_object': depart_object,
                'error': '人数不能为空'
            })
        
        try:
            count_int = int(count)
            if count_int < 0:
                depart_object = models.Department.objects.filter(id=depart_id).first()
                return render(request, 'edit_depart.html', {
                    'depart_object': depart_object,
                    'error': '人数必须为非负数'
                })
        except ValueError:
            depart_object = models.Department.objects.filter(id=depart_id).first()
            return render(request, 'edit_depart.html', {
                'depart_object': depart_object,
                'error': '人数必须为有效数字'
            })
        
        # 更新部门记录
        try:
            models.Department.objects.filter(id=depart_id).update(title=title.strip(), count=count_int)
            return redirect('/depart/')
        except Exception as e:
            depart_object = models.Department.objects.filter(id=depart_id).first()
            return render(request, 'edit_depart.html', {
                'depart_object': depart_object,
                'error': f'更新失败: {str(e)}'
            })


    