#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/15/星期二 13:38
# @Author  : JingQi
# @File    : telecom_platform
# @Software: PyCharm


#!/usr/bin/python
# encoding=utf-8

# 需要执行 pip install --upgrade --no-cache-dir aep-python-sdk-v3
import sys
sys.path.append('..')
from aep_python_sdk_v3 import aep    as apis

if __name__ == '__main__':
    result = apis.aep_device_management.QueryDevice('rir7vzEpGMc','JCI01Nm0B0', '862447066252065')
    print('result='+str(result))