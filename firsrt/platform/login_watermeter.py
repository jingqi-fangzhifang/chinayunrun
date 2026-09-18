#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/18/星期五 11:31
# @Author  : JingQi
# @File    : login_watermeter
# @Software: PyCharm


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2026/9/1/星期二 17:08
# @Author  : JingQi
# @File    : login
# @Software: PyCharm




import requests


def login_and_get_token(company, username, password):
    url = "http://8.154.16.49:10090/zhcbpt/V3/login/login"
    data = {
        "username": username,
        "password": password
    }

    res = requests.post(url, json=data).json()
    # print(res)
    token = res['data']['token']
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Authorization": "Bearer " + token,
        "cookie": "zhcb_meter_web_test_faviconName=favicon; zhcb_meter_web_test_faviconUrl=; zhcb_meter_web_test_token={0}; zhcb_meter_web_test_operatorName=%E7%AE%A1%E7%90%86%E5%91%98; zhcb_meter_web_test_loginName=%E7%AE%A1%E7%90%86%E5%91%98; zhcb_meter_web_test_companyName=%E6%9D%AD%E5%B7%9E%E4%BA%91%E6%B6%A6; zhcb_meter_web_test_companyCount=2; zhcb_meter_web_test_companyId=1; zhcb_meter_web_test_generalRegionId=11; zhcb_meter_web_test_homePageUrl=/zone_measurement/leaking_point/leak_management; zhcb_meter_web_test_homeName=leak_management; zhcb_meter_web_test_systemName=/zone_measurement; zhcb_meter_web_test_initLogin=true; zhcb_meter_web_test_toSystemName=/zone_measurement; zhcb_meter_web_test_fromSystemName=/; zhcb_meter_web_test_AllTreeName=[%22/zone_measurement%22%2C%22leaking_point%22%2C%22leak_management%22%2C%22data_statistics%22%2C%22region_statistics%22%2C%22area_data_analysis%22%2C%22centralized_data_statistics%22%2C%22%22%2C%22%22%2C%22householdTable_data_statistics%22%2C%22%22%2C%22%22%2C%22largeTable_data_statistics%22%2C%22%22%2C%22%22%2C%22householdForm_tableAnalysis%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22singleTable_data_statistics%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22imageRecognition_statistics%22%2C%22dma_alarm_management%22%2C%22alarm_scheme%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22alert_processing%22%2C%22%22%2C%22archives_management%22%2C%22concentrator_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22waterMeter_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22file_change%22%2C%22%22%2C%22%22%2C%22%22%2C%22watermeterProduction_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22equipment_operation%22%2C%22batchValv_control%22%2C%22device_log%22%2C%22electronic_interchange%22%2C%22revenue_data%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22revenue_dataIntegration%22%2C%22%22%2C%22price_management%22%2C%22region_unitprice%22%2C%22payment_inquiry%22%2C%22recharge_payment%22%2C%22platform_management%22%2C%22district_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22personnel_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22role_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22operation_log%22%2C%22/system_setting%22%2C%22system_configuration%22%2C%22platform_dictionary%22%2C%22%22%2C%22%22%2C%22system_parameter%22%2C%22%22%2C%22%22%2C%22alarm_rules%22%2C%22%22%2C%22%22%2C%22permission_configuration%22%2C%22regional_management%22%2C%22%22%2C%22%22%2C%22company_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22function_management%22%2C%22%22%2C%22%22%2C%22personnel_inManagement%22%2C%22%22%2C%22%22%2C%22%22%2C%22%22%2C%22platform_role%22%2C%22%22%2C%22basic_configuration%22%2C%22vendor_management%22%2C%22%22%2C%22%22%2C%22agreement_management%22%2C%22%22%2C%22%22%2C%22application_management%22%2C%22%22%2C%22%22%2C%22instruction_management%22%2C%22%22%2C%22%22%2C%22application_loraWanManagement%22%2C%22%22%2C%22%22%2C%22gateway_management%22%2C%22%22%2C%22%22%2C%22data_interchange%22%2C%22docking_task%22%2C%22%22%2C%22interface_management%22%2C%22%22%2C%22%22%2C%22%22%2C%22/operation_maintenance%22%2C%22operation_inMaintenance%22%2C%22copy_statistics%22%2C%22%22%2C%22sevenDays_withoutReporting%22%2C%22%22%2C%22online_rateStatistics%22%2C%22%22%2C%22archival_statisticsList%22%2C%22%22%2C%22undervoltage_statistics%22%2C%22%22%2C%22zeroWater_statistics%22%2C%22%22%2C%22card_expirationManagement%22%2C%22%22%2C%22inMaintenance_operationLog%22%2C%22imeiQuery%22%2C%22device_operation%22%2C%22send_commands%22%2C%22%22%2C%22equipment_upgrade%22%2C%22app_management%22%2C%22app_management_center%22%2C%22/technological_innovation%22%2C%22technical_innovation%22%2C%22video_chartPicture%22%2C%22secondaryIp_dataOnline%22%2C%22noise_detection%22%2C%22flow_timeStatistics%22%2C%22/zone_metering%22%2C%22overview%22%2C%22region_overview%22]; zhcb_meter_web_test_zone_measurement=/zone_measurement/leaking_point/leak_management; zhcb_meter_web_test_system_setting=/system_setting/system_configuration/platform_dictionary/; zhcb_meter_web_test_operation_maintenance=/operation_maintenance/operation_inMaintenance/copy_statistics/; zhcb_meter_web_test_technological_innovation=/technological_innovation/technical_innovation/video_chartPicture; zhcb_meter_web_test_break=true; zhcb_meter_web_test_zone_metering=/zone_metering/overview/region_overview; zhcb_meter_web_test_pageTitle=%E6%8A%84%E8%A1%A8%E6%80%BB%E8%A7%88".format(
            token)
    }

    return get_rate(company, header=headers)




def get_rate(company,header):

    rate_url = "http://8.154.16.49:10090/zhcbpt/V3/collect/manage/getRateOfDetails"
    res = requests.post(url=rate_url, headers=header).json()
    data_rate = res['data']['totalMeterRate']
    return company + "\t" + str(data_rate)

if __name__ == '__main__':
    # login_and_get_token(username="xHiWuDMXa6fbSfPXzVaIudAgkvekMG3ffcLcXJ6pXe4=", password="gvfuSXWToUYWItZNfaKyHQ==")
    data = {
        "管理员": {"username": "vF8n82f1BjSDMTWSzWuHERO8mu7lsRIp3UqYpM4f1rc=",
                           "password": "gvfuSXWToUYWItZNfaKyHQ=="}
    }
    with open("rate.txt", "a", encoding="utf8") as f:
        for k,v in data.items():
            username = v.get("username")
            password = v.get("password")
            data_file = str(login_and_get_token(company=k,username=username, password=password))

            f.write(data_file + "\n")
        f.close()
