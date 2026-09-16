#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/15/星期二 14:50
# @Author  : JingQi
# @File    : unable_register
# @Software: PyCharm


"""
排查无法注册的问题

登录：https://sso.ctwing.cn/login?service=https%3A%2F%2Fiot.ctwing.cn%2Fapplication%2F#/guide/
电信账号：nwmwater     查询IMEI 是否已存在  如果没有搜出来，那么久返回 没有搜到此IMEI。  如果搜索出来了，就返回 对应的产品名称

1.通过IMEI来查询电信平台是否有此IMEI数据
2.通过IMEI来查询2.0数据库是否有此IMEI数据（现在无法登录2.0平台，这一步先不做）
"""
import sys,json
import aep_device_management
from param import product_master_id,data_login


def get_imei(appKey, appSecret, MasterKey, productId, imei):
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
    return imei, deviceId

if __name__ == '__main__':

    for k,v in product_master_id.items():
        productid = v[0]
        MasterKey = v[1]
        imei, deviceId = get_imei(appKey=data_login['appKey'], appSecret=data_login['appSecret'], MasterKey="fadcf21b42ac48d485ce54ff3646e0be", productId="17315547", imei="862447066252065")
        if imei == deviceId:
            "说明电信平台未查询到此IMEI"
            print(f"平台:{k}\t未获取到IMEI:{imei}")
            # 需要执行其他多个产品的验证
            pass
        else:
            "说明电信平台查询到此IMEI,此时结束循环即可"
            print("平台:{0}：IMIE是:{1}， 对应的设备ID是:{2}".format(k, imei,deviceId))
            break

