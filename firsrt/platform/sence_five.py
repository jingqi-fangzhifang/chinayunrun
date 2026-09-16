#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/16/星期三 14:49
# @Author  : JingQi
# @File    : sence_five
# @Software: PyCharm
"""
场景五：简单场景
登录典型平台通过imei查询其对应的产品
"""
from aep_product_management import QueryProductByImei
from param import data_login

def get_product_by_imei(imei="11862447066252065"):
    data = QueryProductByImei(appKey=data_login["appKey"],appSecret=data_login["appSecret"],imei=imei)
    if data["found"]:
        print("产品名称：", data["productName"], "产品id：", data["productId"])
        return data["productName"], data["productId"]
    else:
        print("未找到对应产品:请核对提供的数据是否准确{0}".format(imei))
        return "未找到对应产品", "请核对提供的数据是否准确：{0}".format(imei)



if __name__ == '__main__':
    # print("场景五：简单场景")
    get_product_by_imei()