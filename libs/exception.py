# 自定义异常处理
from rest_framework.views import exception_handler
from libs.api_response import  APIResponse
from rest_framework import status

# 将仅针对由引发的异常生成的响应调用异常处理程序。它不会用于视图直接返回的任何响应
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    message=""

    # 这个循环是取第一个错误的提示用于渲染


    if response is None:
        return APIResponse(400,"服务器错误",status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=True)
    else:
        for index, value in enumerate(response.data):
            if index == 0:
                key = value
                value = response.data[key]

                if isinstance(value, str):
                    message = value
                    if message == "Authentication credentials were not provided." or message=="Invalid Authorization header. No credentials provided.":
                        message = "用户未登录或登录态失效"
                else:
                    message = value[0]
        # print('123 = %s - %s - %s' % (context['view'], context['request'].method, exc))
        return APIResponse(401,message,status=status.HTTP_200_OK)














