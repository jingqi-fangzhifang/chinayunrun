#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/15/星期二 14:07
# @Author  : JingQi
# @File    : __init__.py
# @Software: PyCharm


import sys
import json
sys.path.append('..')
import aep_device_management

# ==================== 配置区 ====================
appKey = 'rir7vzEpGMc'
appSecret = 'JCI01Nm0B0'
MasterKey = 'fadcf21b42ac48d485ce54ff3646e0be'
productId = '17315547'
imei = '86244706625201165'          # 想查别的 IMEI，直接改这里；也可运行时传参：python imei.py 864390080254840
# ===============================================

if __name__ == '__main__':
    if len(sys.argv) > 1:
        imei = sys.argv[1]

    # 1) IMEI -> deviceId
    deviceId = imei
    lst = aep_device_management.QueryDeviceList(appKey, appSecret, MasterKey,
                                                     productId, imei, 1, 1)
    if lst:
        data = json.loads(lst.decode('utf-8'))
        items = (data.get('result') or {}).get('list') or []
        if items:
            deviceId = items[0]['deviceId']

    # 2) 查设备详情
    result = aep_device_management.QueryDevice(appKey, appSecret, MasterKey,
                                                    productId, deviceId)
    print('imei=%s -> deviceId=%s' % (imei, deviceId))
    print('result=' + (result.decode('utf-8') if result else 'None'))