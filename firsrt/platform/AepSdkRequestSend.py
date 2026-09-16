#!/usr/bin/python
# encoding=utf-8
"""
电信 CTWing(AEP) 开放平台 Python SDK —— 请求签名与发送核心模块
文件来源：中国电信天翼物联网平台官方 Python SDK（apis/AepSdkRequestSend.py）
说明：官方原版，唯一改动是
      1) 时间偏移量 offset 的初始化改为容错处理（离线/网络异常时不阻断 import）
      2) 非 2xx 响应会把平台返回的错误内容带进异常信息，便于排查
"""
import time
import datetime
import base64
import hmac
from hashlib import sha1

import sys

if sys.version_info[0] == 2:
    # Python2
    from urllib import urlencode
    from urllib import quote
    from urlparse import urlparse
    import urllib2
else:
    # Python3
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import urlparse
    import urllib.request as urllib2
    from urllib.error import HTTPError, URLError


baseUrl = 'https://ag-api.ctwing.cn'
timeUrl = 'https://ag-api.ctwing.cn/echo'

sdk = 'GIT: a4fb7fca'
Accept = 'gzip,deflate'
Content_Type = 'application/json; charset=UTF-8'
User_Agent = 'Telecom API Gateway Java SDK'

offset = 0


# key、application、timestamp、body为字符串
# param 为 list，结构如下
# param=[['deviceId', '1'], ['deviceName', 'test']]
def signature(key, application, timestamp, param, body):
    code = "application:" + application + "\n" + "timestamp:" + timestamp + "\n"
    for v in param:
        code += str(v[0]) + ":" + str(v[1]) + "\n"
    if (body is not None) and (body.strip()):
        code += body + '\n'
    return base64.b64encode(hash_hmac(key, code, sha1))


def hash_hmac(key, code, sha1):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1)
    return hmac_code.digest()


def getTimeOffset(url):
    """取平台时间与本机时间的偏移量（毫秒），失败返回 0"""
    try:
        request = urllib2.Request(url)
        start = int(time.time() * 1000)
        response = urllib2.urlopen(request, timeout=10)
        end = int(time.time() * 1000)
        if response is not None:
            return int(int(response.headers['x-ag-timestamp']) - (end + start) / 2)
    except Exception:
        pass
    return 0


# path 为 baseUrl 后面的路径地址字符串，param 用字典，body 为字符串
# （可以为空字符串或者 None，为空时默认为 get 请求）
# version 为字符串（需要去 api 页面查询），application、MasterKey、key 为字符串
def sendSDKRequest(path, head, param, body, version, application, MasterKey, key,
                   method=None, isNeedSort=True, isNeedGetTimeOffset=False):
    paramList = []
    for key_value in param:
        paramList.append([key_value, param[key_value]])
    if (MasterKey is not None) and (MasterKey.strip()):
        paramList.append(['MasterKey', MasterKey])
    if isNeedSort:
        paramList = sorted(paramList)

    headers = {}
    if (MasterKey is not None) and (MasterKey.strip()):
        headers['MasterKey'] = MasterKey
    headers['application'] = application
    headers['Date'] = str(datetime.datetime.now())
    headers['version'] = version

    temp = dict(param.items())
    if (MasterKey is not None) and (MasterKey.strip()):
        temp['MasterKey'] = MasterKey

    url_params = urlencode(temp)

    url = baseUrl + path
    if (url_params is not None) and (url_params.strip()):
        url = url + '?' + url_params

    global offset
    if isNeedGetTimeOffset:
        offset = getTimeOffset(timeUrl)
    timestamp = str(int(time.time() * 1000) + offset)
    headers['timestamp'] = timestamp
    sign = signature(key, application, timestamp, paramList, body)
    if isinstance(sign, bytes):
        sign = sign.decode('utf-8')
    headers['signature'] = sign

    headers.update(head)

    if (body is not None) and (body.strip()):
        request = urllib2.Request(url=url, headers=headers, data=body.encode('utf-8'))
    else:
        request = urllib2.Request(url=url, headers=headers)
    if (method is not None):
        request.get_method = lambda: method

    try:
        response = urllib2.urlopen(request, timeout=30)
    except HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')
        raise RuntimeError('HTTP %s %s -> %s' % (e.code, e.reason, detail))
    except URLError as e:
        raise RuntimeError('网络请求失败: %s' % e)

    if ('response' in vars()):
        return response
    else:
        return None


# 模块导入时同步一次平台时间偏移（官方行为，这里做容错）
try:
    offset = getTimeOffset(timeUrl)
except Exception:
    offset = 0
