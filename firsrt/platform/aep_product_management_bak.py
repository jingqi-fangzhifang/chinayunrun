#!/usr/bin/python
# encoding=utf-8
"""
电信 CTWing(AEP) 开放平台 Python SDK —— 产品管理模块
文件对应官方 SDK 的 apis/aep_product_management_bak.py

QueryProduct     产品详情：GET /aep_product_management/product      version 20181031202055
QueryProductList 产品列表：GET /aep_product_management/products     version 20190507004824
注意：这两个查询接口只需要应用级鉴权（appKey/appSecret），不需要 MasterKey。
"""
try:
    from . import AepSdkRequestSend
except (ImportError, ValueError):
    import AepSdkRequestSend

# 同一路径 /product 下按 HTTP 方法区分接口，version 各不相同
#   GET    /product  查询产品详情  20181031202055
#   POST   /product  创建产品      20191018204154
#   PUT    /product  修改产品      20191018204806
#   DELETE /product  删除产品      20181031202029
VERSION_PRODUCT_QUERY = '20181031202055'
VERSION_PRODUCT_LIST = '20190507004824'


def QueryProduct(appKey, appSecret, productId):
    """查询单个产品详情"""
    path = '/aep_product_management/product'
    head = {}
    param = {'productId': productId}
    version = VERSION_PRODUCT_QUERY
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version,
                                                application, None, key, 'GET')
    if response is not None:
        return response.read()
    return None


def QueryProductList(appKey, appSecret, searchValue, pageNow, pageSize):
    """查询产品列表"""
    path = '/aep_product_management/products'
    head = {}
    param = {'searchValue': searchValue, 'pageNow': pageNow, 'pageSize': pageSize}
    version = VERSION_PRODUCT_LIST
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version,
                                                application, None, key, 'GET')
    if response is not None:
        return response.read()
    return None
