"""besettest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from users import  views
from django.contrib import admin
from django.conf.urls import url,include
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url('admin/', admin.site.urls),  #admin后台url
    url(r"^docs/", include_docs_urls(title="infaterText")),  # 文档配置
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")), #配置之后文档就可以登录了
    url(r'^users/login/', obtain_jwt_token),  #生成token并验证
    url(r"^users/registers/", views.Registers.as_view(), name="Register"),
    url(r"^users/department/", views.Department.as_view(), name="Department"),


]
