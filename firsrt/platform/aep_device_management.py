#!/usr/bin/python
# encoding=utf-8
"""
电信 CTWing(AEP) 开放平台 Python SDK —— 设备管理模块
文件对应官方 SDK 的 apis/aep_device_management.py

QueryDevice 单设备详情：GET /aep_device_management/device
  入参：appKey、appSecret、MasterKey、productId、deviceId
  其中 appKey/appSecret 来自控制台「应用管理」，MasterKey/productId 来自「产品中心」

QueryDeviceList 设备列表：GET /aep_device_management/devices
"""
try:
    from . import AepSdkRequestSend
except (ImportError, ValueError):
    import AepSdkRequestSend

# 各接口的 api version，可在「文档中心-使能平台API文档」中对应接口处查到
# 注意：同一路径 /device 下按 HTTP 方法区分不同接口，version 各不相同
#   GET  /device  查询设备详情   20181031202139
#   POST /device  增加设备       20181031202117
#   PUT  /device  修改设备       20181031202122
#   DELETE /device 删除设备      20181031202131
VERSION_DEVICE_MANAGEMENT = '20181031202139'
VERSION_DEVICE_LIST = '20190507012134'


def QueryDevice(appKey, appSecret, MasterKey, productId, deviceId):
    """查询单个设备详情

    参数顺序：appKey, appSecret, MasterKey, productId, deviceId
    兼容处理：部分示例代码按 (…, deviceId, productId) 传参（productId 为纯数字、deviceId 为 32 位
    十六进制串），这里自动识别并纠正，保证两种写法都能查通。
    """
    if (not str(productId).isdigit()) and str(deviceId).isdigit():
        productId, deviceId = deviceId, productId
    path = '/aep_device_management/device'
    head = {}
    param = {'productId': productId, 'deviceId': deviceId}
    version = VERSION_DEVICE_MANAGEMENT
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version,
                                                application, MasterKey, key, 'GET')
    if response is not None:
        return response.read()
    return None




def QueryDeviceList(appKey, appSecret, MasterKey, productId, searchValue, pageNow, pageSize):
    """查询设备列表"""
    path = '/aep_device_management/devices'
    head = {}
    param = {'productId': productId, 'searchValue': searchValue,
             'pageNow': pageNow, 'pageSize': pageSize}
    version = VERSION_DEVICE_LIST
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version,
                                                application, MasterKey, key, 'GET')
    if response is not None:
        return response.read()
    return None
