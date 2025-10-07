from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
class AuthMiddleware(MiddlewareMixin):
    """用户认证中间件"""
    def process_request(self,request):
        #先对不用登陆就可以访问的界面进行处理
        if request.path_info in ["/login/","/img/code/"]:
            return None
        #再对需要登陆才可以访问的界面进行处理
        info_dict = request.session.get("userInfo")
        if not info_dict:
            return redirect("/login/")
        request.userInfo = info_dict
        return None