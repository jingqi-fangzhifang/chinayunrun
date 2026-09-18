#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/18/星期五 13:41
# @Author  : JingQi
# @File    : unsubscrib
# @Software: PyCharm

"""
无法注销问题
"""
from aep_product_management import QueryProductByImei
from param import data_login


def unsubscribe_by_imei(imei):
    # {'imei': '862447066252065', 'found': True, 'productId': 17315547, 'productName': '宁水常规小表3', 'deviceId': 'e6d0e42e0fd643ad8bb02410ab965470', 'deviceName': '862447066252065', 'MasterKey': 'fadcf21b42ac48d485ce54ff3646e0be', 'matched': [(17315547, '宁水常规小表3', 'fadcf21b42ac48d485ce54ff3646e0be')], 'scanned': 276, 'errors': []}
    result = QueryProductByImei(appKey=data_login['appKey'], appSecret=data_login['appSecret'], imei=imei)
    if result['found'] == 200:
        pass
