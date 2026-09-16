#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/3/星期四 11:20
# @Author  : JingQi
# @File    : login_internet_of_thing
# @Software: PyCharm
import json
from datetime import datetime

import requests
from requests.sessions import session
from param import internet_of_things_param
session_requests = session()


base_url = "http://8.149.238.245:10090"
# 登录物联网平台
def login_internet_of_thing():
    url = base_url + "/wateriot/system/login"
    data = {
        "username": internet_of_things_param['账号'],
        "password": internet_of_things_param["密码"]
        }
    # data_t = json.loads(data)

    response = session_requests.post(url, data=data).json()
    print(response)


def get_deviceId(code="0859002027"):
    url = base_url + "/wateriot/device/device/pageDeviceSimplify?offset=1&limit=20&deviceInfo=" + code
    response = session_requests.get(url).json()
    print("-----------------------------------")
    print(response)
    print("-----------------------------------")
    if len(response['data']) > 0:
        return response["data"][0]["deviceId"]
    else:
        return None



def get_log(deviceId,start_time,end_time):
    # date_time = datetime.now().strftime("%Y-%m-%d")
    try:
        url = base_url + "/wateriot/business/uploadData/queryUploadData?offset=1&limit=20&deviceId={0}&startTime={1}+00:00:00&endTime={2}+23:59:59".format(deviceId,start_time, end_time)
        response_dict = session_requests.get(url).json()
        print("-----------------------")

        data = response_dict['data']['list'][-1]['deviceData']
        print(data)
        dict_data = json.loads(data)

        # print(dict_data['meterDataList'][-1]["flowList"][-1]['collectingTime'],dict_data,response_dict, end="\n")
        return dict_data['meterDataList'][-1]["flowList"][-1]['collectingTime'], dict_data,response_dict
    except Exception as e:
        print(e)
        # 异常情况说明 取不到日志数据，大概率就是 运营商平台问题
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S"), dict_data,response_dict


def main_of_thing(deviceCode,start_time=datetime.now().strftime("%Y-%m-%d"),end_time=datetime.now().strftime("%Y-%m-%d")):
    login_internet_of_thing()
    deviceId = get_deviceId(deviceCode)
    times, dates,res = get_log(deviceId,start_time,end_time)
    print(times)
    return times, dates,res


if __name__ == '__main__':
    main_of_thing()
