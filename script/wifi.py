# coding:utf8
# author:Xu YiQing
# python version:2.7

"""
    Dietpi Config Server Copyright 2004-2019 Dreamtech.

    Licensed under the Apache License, Version 2.0 (the "License");
    You may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import os
import time
import utils.charset_util as uc


def modify_wifi(ssid, password):
    """
    配置WIFI
    :param ssid: SSID
    :param password: 密码
    :return:
    """
    f = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r+')
    f.truncate()
    f.write(
        "country=CN\r\n" +
        "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\r\n" +
        "update_config=1\r\n" +
        "network={\r\n" +
        "ssid=\"" + ssid + "\"\r\n" +
        "scan_ssid=1\r\n" +
        "key_mgmt=WPA-PSK\r\n" +
        "psk=\"" + password + "\"\r\n" +
        "}"
    )
    f.close()
    time.sleep(1)
    os.popen("killall wpa_supplicant")
    time.sleep(2)
    # os.popen("wpa_supplicant -Dnl80211 -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -B")
    os.popen("wpa_supplicant -Dnl80211 -i wlan1 -c /etc/wpa_supplicant/wpa_supplicant.conf -B")


def get_wifi_list():
    """
    查询局域网内可用的WIFI
    :return: WIFI的SSID列表
    """
    # result = os.popen('iw dev wlan0 scan | grep SSID').read()
    result = os.popen('iw dev wlan1 scan | grep SSID').read()
    temp = result.split('\n')
    results = []
    for item in temp:
        if "\\x00" not in item:
            if item.strip() == "":
                continue
            if item.strip() == "SSID:":
                continue
            temp_ssid = item.strip().split("SSID: ")[1]
            if temp_ssid.startswith("\\x"):
                ssid = uc.str_to_chinese(temp_ssid)
            else:
                ssid = temp_ssid
            results.append(ssid)
    return results


def check_wifi():
    """
    查找当前的WIFI
    :return:
    """
    # result = os.popen('wpa_cli -i wlan0 status').read()
    result = os.popen('wpa_cli -i wlan1 status').read()
    temp = result.split("bssid=")[1].split("ssid=")[1].split("id=")[0]
    return temp.strip()


def disconnect():
    """
    断开连接（等待3秒）
    :return:
    """
    # os.popen("wpa_cli -i wlan0 disable_network 0")
    os.popen("wpa_cli -i wlan1 disable_network 0")
    time.sleep(1)
    # os.popen("wpa_cli -i wlan0 remove_network 0")
    os.popen("wpa_cli -i wlan1 remove_network 0")
    time.sleep(1)
    # os.popen("wpa_cli -i wlan0 save_config")
    os.popen("wpa_cli -i wlan1 save_config")
