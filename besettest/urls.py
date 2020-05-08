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

from django.conf.urls import url,include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from project import views as projectViews
from users import  views as userViews


urlpatterns = [
    url('admin/', admin.site.urls),  #admin后台url
    url(r"^docs/", include_docs_urls(title="InterfaceText")),  # 文档配置
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")), #配置之后文档就可以登录了
    url(r'^users/login/$', obtain_jwt_token),  #生成token并验证
    url(r"^users/registers/", userViews.Registers.as_view(), name="Register"),
    url(r"^users/department/", userViews.Department.as_view(), name="Department"),
    #project
    url(r"^users/project_list/", projectViews.ProjectList.as_view(), name="ProjectList"),
    url(r"^users/add_project/", projectViews.AddProject.as_view(), name="ProjectAdd"),
    url(r"^users/edit_project/", projectViews.EditProject.as_view(), name="ProjectEdit"),
    url(r"^users/remove_project/", projectViews.RmoveProject.as_view(), name="ProjectRemove"),
    url(r"^users/last_use_project/", projectViews.LastProject.as_view(), name="ProjectLast"), #用户最后使用项目记录
    #files文件夹操作
    url(r"^users/post_methods/", projectViews.PostMethods.as_view(), name="PostMethods"),  # 请求数据集
    url(r"^users/add_file/", projectViews.addFilesName.as_view(), name="addFiles"),  # 新增接口文件夹
    url(r"^users/edit_file/", projectViews.EditFilesName.as_view(), name="EditFilesName"),  # 编辑接口文件夹
    url(r"^users/remove_file/", projectViews.RemoveFilesName.as_view(), name="RemoveFilesName"),  # 移除接口文件夹
    url(r"^users/select_file/", projectViews.SelectFilesName.as_view(), name="SelectFilesName"),  # 查看接口返回类容
    #接口文件操作
    url(r"^users/add_files/", projectViews.addFiles.as_view(), name="addFiles"),  # 新增接口文件
    url(r"^users/edit_files/", projectViews.EditFiles.as_view(), name="EditFiles"),  # 编辑接口文件
    url(r"^users/remove_files/", projectViews.RmoveFiles.as_view(), name="RmoveFiles"),  # 删除接口文件
    url(r"^users/copy_files/", projectViews.CopyFiles.as_view(), name="CopyFiles"),  # 复制接口文件
    #接口文档详情
    url(r"^users/interface_detail/", projectViews.InterfaceDetailGet.as_view(), name="InterfaceDetailGet"),  # 接口文档详情
    url(r"^users/edit_interface_detail/", projectViews.EditInterfaceDetail.as_view(), name="EditInterfaceDetail"),  # 修改接口文档数据
    #模拟请求数据
    url(r"^users/mock_requests/", projectViews.MockPost.as_view(), name="MockPost"),#模拟请求数据
    url(r"mock/$", projectViews.MockRes.as_view(), name="MockRes"), #模拟返回数据
    #修改mock返回类型以及对应的返回数据
    url(r"^users/mock_update_type/", projectViews.MockResData.as_view(), name="MockResData"),  # 修改mock返回类型以及对应的返回数据
    #环境变量操作
    url(r"^users/environment_add/", projectViews.EnvironmentsAdd.as_view(), name="EnvironmentsAdd"),#新增环境
    url(r"^users/environment_select/", projectViews.EnvironmentsSelect.as_view(), name="EnvironmentsSelect"),  # 查询环境

    url(r"^users/environment_delete", projectViews.EnvironmentsDelete.as_view(), name="EnvironmentsDelete"),  # 查询环境

]
