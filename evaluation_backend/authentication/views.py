# authentication/views.py

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers

# 简化的用户序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id']

class LoginView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': '请输入用户名和密码'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return Response({
                'success': True,
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'success': False,
                'error': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = [AllowAny]  # 允许未认证用户使用注销功能
    
    def post(self, request):
        logout(request)
        return Response({'success': True})

class UserView(views.APIView):
    """获取当前用户信息"""
    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)

class UserListView(views.APIView):
    """用户管理：列出所有用户"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)
    
    def post(self, request):
        """创建新用户"""
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username or not password:
            return Response({'error': '用户名和密码不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return Response({
            'success': True,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class UserDetailView(views.APIView):
    """用户管理：删除用户"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            # 不允许删除自己
            if user == request.user:
                return Response({'error': '不能删除当前登录的用户'}, status=status.HTTP_400_BAD_REQUEST)
                
            user.delete()
            return Response({'success': True})
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)