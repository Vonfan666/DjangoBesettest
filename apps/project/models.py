from django.db import models
# Create your models here.

class ProjectList(models.Model):
    name=models.CharField(max_length=20,verbose_name="项目名称")
    dev_attr=models.CharField(max_length=100,verbose_name="开发地址")
    test_attr=models.CharField(max_length=100,verbose_name="测试地址")
    product_attr=models.CharField(max_length=100,verbose_name="生产地址")
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    user=models.ForeignKey("users.UserProfile",to_field="id",on_delete=models.SET_DEFAULT,default=1,verbose_name="创建用户id")
    class Meta:
        db_table= "project_list"
