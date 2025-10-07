from django.db import models
class UserInfo(models.Model):
    name = models.CharField(verbose_name='性别',max_length=12)
    age = models.IntegerField(verbose_name='年龄')  
    email = models.EmailField(verbose_name='邮箱',max_length=32)
# Create your models here.
class Department(models.Model):
    title = models.CharField(verbose_name='部门名称',max_length=12)
    count = models.IntegerField(verbose_name='人数')