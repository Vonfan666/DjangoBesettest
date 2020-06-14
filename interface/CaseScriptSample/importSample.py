import json,time,logging,unittest,os,sys
from case import models,serializers
from case.libs.toRequests import InRequests
from libs.api_response import APIResponse
from  rest_framework.views import APIView,status
import time
from case.libs.findeSqlCase import CaseAction
from log.logFile import logger as logs
s=CaseAction()