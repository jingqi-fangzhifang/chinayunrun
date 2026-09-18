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
    # print(response)


def get_thirdDeviceId(imei):
    try:
        url = base_url + "/wateriot/device/device/pageDeviceSimplify?offset=1&limit=20&deviceInfo={0}".format(imei)
        response_list = session_requests.get(url).json()['data']
        if len(response_list)>0:
            print(response_list[0]['thirdDeviceId'])
            return response_list[0]['thirdDeviceId'], response_list[0]['deviceId']
        return None,None
    except Exception as e:
        return None,None


def get_log(deviceId,start_time,end_time):

    """
    根据设备ID和时间范围获取设备日志数据

    参数:
        deviceId (str): 设备标识ID
        start_time (str): 开始时间，格式为"YYYY-MM-DD"
        end_time (str): 结束时间，格式为"YYYY-MM-DD"

    返回:
        tuple: 包含三个元素的元组
            - collectingTime (str): 最后一条数据的采集时间
            - dict_data (dict): 解析后的设备数据字典
            - response_dict (dict): 原始API响应数据
        如果发生异常则返回 (None, None)
    """
    # date_time = datetime.now().strftime("%Y-%m-%d")  # 这行代码被注释掉了，可能是用于获取当前日期的
    try:
        # 构造API请求URL，包含设备ID和时间范围参数
        url = base_url + "/wateriot/business/uploadData/queryUploadData?offset=1&limit=20&deviceId={0}&startTime={1}+00:00:00&endTime={2}+23:59:59".format(deviceId,start_time, end_time)
        # 发送GET请求并获取响应的JSON数据
        response_dict = session_requests.get(url).json()
        print("-----------------------", response_dict)
        # 从响应数据中提取最新的设备数据
        data = response_dict['data']['list'][-1]['deviceData']
        print(data)
        # 将JSON格式的设备数据解析为Python字典
        dict_data = json.loads(data)
        print(dict_data)
        # print(dict_data['meterDataList'][-1]["flowList"][-1]['collectingTime'],dict_data,response_dict, end="\n")  # 这行代码被注释掉了，可能是用于调试打印
        # 返回采集时间、解析后的数据字典和原始响应数据
        return response_dict['data']['list'][-1]['receiveTime'], dict_data,response_dict
    except Exception as e:
        # 打印异常信息
        print(e)
        # 异常情况说明 取不到日志数据，大概率就是 运营商平台问题
        return None,None,None



def main_of_thing(imei="862447066252065",start_time=datetime.now().strftime("%Y-%m-%d"),end_time=datetime.now().strftime("%Y-%m-%d")):
    login_internet_of_thing()
    # deviceId = get_deviceId(deviceCode)
    thirdDeviceId,deviceId = get_thirdDeviceId(imei)
    print(thirdDeviceId,deviceId)
    if deviceId:
        data = get_log(deviceId,start_time=start_time, end_time=end_time)
        return thirdDeviceId,data
    return thirdDeviceId,()


if __name__ == '__main__':
    print(main_of_thing())
    # login_internet_of_thing()
    # third,deviceid = get_thirdDeviceId("862447066252065")
    # print("+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print(third,deviceid)
    # aa,bb,cc = get_log(deviceId=deviceid,start_time=datetime.now().strftime("%Y-%m-%d"),end_time=datetime.now().strftime("%Y-%m-%d"))
    # print(aa,bb,cc)
