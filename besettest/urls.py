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
# from django.urls import path,
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from project import views as projectViews
from users import  views as userViews
from case import  views as caseViews
from case  import  runCase
# from case import tasks

urlpatterns = [
    url('admin/', admin.site.urls),  #admin后台url
    #将websocket协议指向websocketUrls
    # url(r'^ws/', include('besettest.websocketUrls')),
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
    url(r"^users/unity_project/", projectViews.ProjectUnityStatus.as_view(), name="ProjectLast"),  # 修改同步状态

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
    url(r"^users/environment_delete/", projectViews.EnvironmentsDelete.as_view(), name="EnvironmentsDelete"),  # 删除环境变量
    url(r"^users/aa/", projectViews.MenuView.as_view(), name="View"),  # 查询环境
    #case操作
    url(r"^users/unity_project/", projectViews.ProjectUnityStatus.as_view(), name="ProjectUnityStatus"),  # 查询用例以及用例文件下的用例
    url(r"^users/select_caseGroup/", caseViews.CaseGroup.as_view(), name="CaseGroup"),  # 查询用例以及用例文件下的用例
    url(r"^users/caseGroup_add/", caseViews.AddGroup.as_view(), name="AddGroup"),  # 新增用例文件夹
    url(r"^users/caseGroup_edit/", caseViews.EditGroup.as_view(), name="EditGroup"),  # 修改用例文件夹
    url(r"^users/caseGroup_remove/", caseViews.RemoveGroup.as_view(), name="RemoveGroup"),  # 删除用例文件夹
    url(r"^users/caseInterface_add/", caseViews.AddInterface.as_view(), name="AddCase"),  # 新增用例接口
    url(r"^users/caseInterface_edit/", caseViews.EditCase.as_view(), name="EditCase"),  # 编辑接口名称
    url(r"^users/caseInterface_remove/", caseViews.RemoveInterface.as_view(), name="RemoveInterface"),  # 删除接口
    url(r"^users/case_add/", caseViews.AddCase.as_view(), name="AddInterface"),  # 新增用例文件
    url(r"^users/case_list/", caseViews.CaseList.as_view(), name="CaseList"),  # 查看用例列表
    url(r"^users/case_remove/", caseViews.CaseRemove.as_view(), name="CaseRemove"),  # 删除用例
    url(r"^users/case_edit/", caseViews.CaseEdit.as_view(), name="CaseEdit"),  # 点击编辑用例
    url(r"^users/case_run/", caseViews.RunCase.as_view(), name="RunCase"),  # 执行单个接口下所有用例
    url(r"^users/case_debug/", caseViews.DebugCase.as_view(), name="DebugCase"),  # 用例调试
    url(r"^users/case_results/", caseViews.CaseResults.as_view(), name="CaseResults"),  # 查看用例调试结果
    url(r"^users/case_results_detail/", caseViews.CaseResultsDetail.as_view(), name="CaseResultsDetail"),  # 查看debug日志详情

    url(r"^users/case_results_del/", caseViews.CaseResults.as_view(), name="CaseResults"),  # 查看删除用例调试
    # url(r"^users/case_run_all/", runCase.RunCaseAll.as_view(), name="RunCaseAll"),  # 执行测试计划
    # url(r"^users/case_run_all/", tasks.UsersTask.as_view(), name="RunCaseAll"),  # 执行测试计划
    url(r"^users/case_run_all/", caseViews.RunAll.as_view(), name="RunCaseAll"),  # 异步执行测试计划
    url(r"^users/timed_task/", caseViews.TimedTask.as_view(), name="TimedTask"),  # 新增定时任务

    url(r"^users/case_order/", caseViews.CaseOrder.as_view(), name="CaseOrder"),  # 修改该接口的执行顺序
    url(r"^users/casePlan_add/", caseViews.AddCasePlan.as_view(), name="AddCasePlan"),  # 新建测试计划
    url(r"^users/casePlan_get/", caseViews.GetCasePlan.as_view(), name="GetCasePlan"),  # 查看测试计划
    url(r"^users/casePlan_edit/", caseViews.UpdateCasePlan.as_view(), name="UpdateCasePlan"),  # 编辑测试计划
    url(r"^users/casePlan_delete/", caseViews.DeleteCasePlan.as_view(), name="DeleteCasePlan"),  # 删除测试计划
    url(r"^users/caseList_get/", caseViews.GetCaseList.as_view(), name="GetCaseList"),  # 查看项目下的用例列表
    url(r"^users/caseOrder_edit/", caseViews.EditCaseOrder.as_view(), name="EditCaseOrder"),  # 编辑接口和用例的执行顺序
    #自己的定时任务列表
    url(r"^users/add_timedTask/", caseViews.addTimedTask.as_view(), name="addTimedTask"),  # 新增自己的定时任务列表
    url(r"^users/get_timedTask/", caseViews.GetTimedTask.as_view(), name="GetTimedTask"),  # 查看自己的定时任务
    url(r"^users/remove_timedTask/", caseViews.RemoveTimedTask.as_view(), name="RemoveTimedTask"),  # 删除自己的定时任务
    url(r"^users/update_timedTask/", caseViews.UpdateTimedTask.as_view(), name="UpdateTimedTask"),  # 编辑自己的定时任务

    url(r"^users/valid_cron/", caseViews.ValidCron.as_view(), name="ValidCron"),  # 校验cron

]
