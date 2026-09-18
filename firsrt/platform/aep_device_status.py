#!/usr/bin/python
# encoding=utf-8
"""
电信 CTWing(AEP) 开放平台 Python SDK —— 设备状态模块
文件对应官方 SDK 的 apis/aep_device_status.py

本机实测（2026-09-16，真实凭据，均返回 code=0）：

  接口                        作用                 method  path                                              version
  QueryDeviceStatus           查询设备最新状态     POST    /aep_device_status/deviceStatus                    20181031202028
  getDeviceStatusHisInTotal   查询历史数据(不分页) POST    /aep_device_status/api/v1/getDeviceStatusHisInTotal 20190928013529
  getDeviceStatusHisInPage    查询历史数据(分页)   POST    /aep_device_status/getDeviceStatusHisInPage        20190928013337

三个坑，都踩过了：
  1) 本模块接口【不传 MasterKey】（传 None）。与设备管理类接口（必须带 MasterKey）不同。
  2) `/api/v1/` 前缀在这一组里并不统一：getDeviceStatusHisInTotal 有、getDeviceStatusHisInPage 没有，
     给分页接口加 /api/v1/ 会 404「Api version not found」。
  3) getDeviceStatusHisInPage 的 page_timestamp 只能传上一页返回的值；首页请不要传该字段
     （官方 demo 里那个写死的 2018 年时间戳会让结果永远是空列表 []）。
"""

try:
    from . import AepSdkRequestSend
except (ImportError, ValueError):
    import AepSdkRequestSend

VERSION_DEVICE_STATUS = '20181031202028'
VERSION_STATUS_HIS_TOTAL = '20190928013529'
VERSION_STATUS_HIS_PAGE = '20190928013337'


def QueryDeviceStatus(appKey, appSecret, body):
    """查询设备最新状态

    body 为 JSON 字符串，需包含 productId、deviceId、datasetId。
    示例：{"productId":"17315547","deviceId":"e6d0...","datasetId":"signalStrength"}
    """
    path = '/aep_device_status/deviceStatus'
    version = VERSION_DEVICE_STATUS
    response = AepSdkRequestSend.sendSDKRequest(path, {}, {}, body, version,
                                                appKey, None, appSecret, 'POST')

    if response is not None:
        return response.read()
    return None


def getDeviceStatusHisInTotal(appKey, appSecret, body):
    """查询设备历史数据（不分页）

    body 为 JSON 字符串，需包含 productId、deviceId、datasetId，
    可选 begin_timestamp / end_timestamp（13 位毫秒）。
    """
    path = '/aep_device_status/api/v1/getDeviceStatusHisInTotal'
    version = VERSION_STATUS_HIS_TOTAL
    response = AepSdkRequestSend.sendSDKRequest(path, {}, {}, body, version,
                                                appKey, None, appSecret, 'POST')
    if response is not None:
        return response.read().decode('utf-8')
    return None


def getDeviceStatusHisInPage(appKey, appSecret, body):
    """查询设备历史数据（分页）

    body 为 JSON 字符串：productId、deviceId、begin_timestamp、end_timestamp、page_size。
    首页不要传 page_timestamp；翻页时传上一页响应里的 page_timestamp。
    """
    path = '/aep_device_status/getDeviceStatusHisInPage'
    version = VERSION_STATUS_HIS_PAGE
    response = AepSdkRequestSend.sendSDKRequest(path, {}, {}, body, version,
                                                appKey, None, appSecret, 'POST')

    if response is not None:
        return response.read().decode('utf-8')
    return None


if __name__ == '__main__':
    print(getDeviceStatusHisInPage('rir7vzEpGMc', 'JCI01Nm0B0', '{"productId":"17315547","deviceId":"e6d0e42e0fd643ad8bb02410ab965470","begin_timestamp":1789009393000,"end_timestamp":1789527793000,"page_size":5}'))