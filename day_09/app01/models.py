from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=32)

class Department(models.Model):
    title = models.CharField(verbose_name="部门名称",max_length=32)
    count = models.IntegerField(verbose_name="部门人数",default=0)