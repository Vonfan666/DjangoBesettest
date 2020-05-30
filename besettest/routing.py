# #!/usr/bin/python3
# # @File:.py
# # -*- coding:utf-8 -*-
# # @Author:von_fan
# # @Time:2020年05月30日22时34分28秒

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from . import websocketUrls

application = ProtocolTypeRouter({
    # 普通的HTTP协议在这里不需要写，框架会自己指明
    'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(
        URLRouter(
        	# 指定去对应应用的routing中去找路由
             websocketUrls.urlpatterns
        	)
		),
    )
})

