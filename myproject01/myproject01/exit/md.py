from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 定义不需要登录验证的URL白名单
        white_list = ['/login/', '/admin/']
        
        # 如果当前请求的URL在白名单中，直接放行
        if request.path_info in white_list: 
            return None
            
        # 检查用户是否已登录
        info_dict = request.session.get("info")
        if info_dict:
            # 已登录用户，继续处理请求
            request.info = info_dict
            return None
        else:
            # 未登录用户，重定向到登录页面
            return redirect("/login/")
    
    def process_response(self, request, response):
        return response