from django.db import models

class Department(models.Model):
    """部门表"""
    title = models.CharField(max_length=32, verbose_name="部门名称")
    def __str__(self):
        return self.title
class Admin(models.Model):
    """管理员表"""
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    gender = models.IntegerField(
        verbose_name="性别",
        choices=[(1,"男"),(0,"女")]
    )
    depart = models.ForeignKey(
        verbose_name="部门",
        to="Department",
        on_delete=models.CASCADE
    )
class Phone(models.Model):
    """手机号表"""
    mobile = models.CharField(max_length=11,verbose_name="手机号")
    price = models.PositiveIntegerField(verbose_name="价格",default=0)
    level = models.SmallIntegerField(
        verbose_name="等级",
        choices=[(1,"一级"),(2,"二级"),(3,"三级"),(4,"四级")],
        default=1
        )
    status = models.BooleanField(verbose_name="状态",default=False)
    admin = models.ForeignKey(
        verbose_name="管理员",
        to="Admin",
        on_delete=models.CASCADE
    )

