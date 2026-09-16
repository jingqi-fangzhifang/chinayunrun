#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/15/星期二 15:58
# @Author  : JingQi
# @File    : unable_unregister
# @Software: PyCharm
"""
3： 场景（AEP) 售后反馈：注销不了
查询在电信平台上IMEI 是否已存在   如果不存在，返回 没有搜索到此IMEI。      如果存在，要对比电信上这个IMEI的 设备ID，跟 物联网 这个IMEI的设备ID 是否一致，返回结果就行。
"""

import sys,json
import aep_device_management
from param import product_master_id,data_login
from platform_login import main_of_thing


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
        imei, deviceId = get_imei(appKey=data_login['appKey'], appSecret=data_login['appSecret'], MasterKey="fadcf21b42ac48d485ce54ff3646e0be", productId="17315547", imei="11862447066252065")
        if imei == deviceId:
            "说明电信平台未查询到此IMEI"
            print(f"平台:{k}\t未获取到IMEI:{imei}")
            # 需要执行其他多个产品的验证
            pass
        else:
            "说明电信平台查询到此IMEI,此时结束循环即可"
            print("平台:{0}：IMIE是:{1}， 对应的设备ID是:{2}".format(k, imei,deviceId))
            # 这里进行判断： 如何电信平台的设备ID == 物联网的第三方设备ID 说明物联网上的物联网同步了电信数据
            third_platform_device_id,data = main_of_thing(imei)
            if third_platform_device_id == deviceId:
                print("物联网平台同步了电信平台的数据")
            else:
                print("物联网平台未同步电信平台的数据")
            break
