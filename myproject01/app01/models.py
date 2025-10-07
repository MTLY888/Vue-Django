from tabnanny import verbose
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    #用户信息表
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=32)
