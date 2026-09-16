#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/15/星期二 17:12
# @Author  : JingQi
# @File    : scene_four
# @Software: PyCharm
"""
场景4
4： 场景：（AEP）售后反馈现场激活02，平台没数据。  1：拿IMEI查询 物联网是否有日志  --有的话，把最新日志拉出   没有的话，去电信查是否有数据包
输入IMEI 搜错所属产品，点进产品，设备管理，输入IMEI，点击IMEI蓝色字体 跳转单表查看--数据查看

"""
import json

from aep_product_management import QueryProductByImei
from platform_login import main_of_thing
from aep_device_status import getDeviceStatusHisInPage
from param import data_login
from datetime import datetime, timedelta

def get_tuple_time():
    # 当天零点
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # 当天最后一刻（23:59:59.999）
    today_end = today_start + timedelta(days=1) - timedelta(microseconds=1)

    # 转13位毫秒时间戳
    start_ts = int(today_start.timestamp() * 1000)
    end_ts = int(today_end.timestamp() * 1000)

    return start_ts, end_ts


def get_history_data(appKey, appSecret, body):
    """

    :param appKey:
    :param appSecret:
    :param body: '{"productId":"17315547","deviceId":"e6d0e42e0fd643ad8bb02410ab965470","begin_timestamp":1789009393000,"end_timestamp":1789527793000,"page_size":5}'
    :return:
    """
    return getDeviceStatusHisInPage(appKey, appSecret, body)

def main(imei="11862447066252065"):
    third_platform_deviceid, message = main_of_thing(imei=imei)
    # 通过imei 获取到deviceId
    # 通过imei 获取到产品 {'imei': '862447066252065', 'found': True, 'productId': 17315547, 'productName': '宁水常规小表3', 'deviceId': 'e6d0e42e0fd643ad8bb02410ab965470', 'deviceName': '862447066252065', 'matched': [(17315547, '宁水常规小表3')], 'scanned': 276, 'errors': []}
    data = QueryProductByImei(appKey=data_login['appKey'],
        appSecret=data_login['appSecret'],
                       imei=imei)
    # print(message, data)
    if message is None:
        if data['found']:
            # 说明获取到了数据 productId deviceId

            # 说明物理网上没以后数据
            # 此时应该去登录 电信平台，查询是否有数据包
            st, et = get_tuple_time()
            body = {"productId": data['productId'], "deviceId": data['deviceId'], "begin_timestamp": st,
                    "end_timestamp": et, "page_size": 5}
            deviceStatusList = get_history_data(appKey=data_login['appKey'],
                             appSecret=data_login['appSecret'],
                             body=json.dumps(body))
            list_data = json.loads(deviceStatusList)
            # print(list_data)
            if list_data.get("deviceStatusList",None) is not None:
                # 说明电信平台有数据
                # print("物联网数据为空，第三方电信平台数据为{}".format(str(deviceStatusList)))
                return  "物联网平台没有数据此imei数据 {}".format(imei),"电信平台的数据为：" + str(list_data['deviceStatusList'])
            # 则说明物联网没有同步电信的数据

            return  "物联网平台没有数据此imei数据 {}".format(imei),"电信平台也为查询到该imei对应的数据，此时电信平台响应的结果为\t" + str(deviceStatusList)
        return "物联网平台没有数据此imei数据 {}".format(imei)
    else:
        # 说明物联网平台有数据
        print("物联网平台数据为{}".format(str(message)))
        return "物联网平台数据为{}，说明已同步电信平台数据".format(str(message))


if __name__ == '__main__':
    print(main())