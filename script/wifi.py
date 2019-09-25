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
import utils.charset_util as uc
import utils.log_util as log


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
    log.log("Update New WIFI Config File Success!", log.INFO_LEVEL)


def get_wifi_list():
    """
    查询局域网内可用的WIFI
    :return: WIFI的SSID列表
    """
    result = os.popen('iw dev wlan0 scan | grep SSID').read()
    temp = result.split('\n')[:-1]
    results = []
    for item in temp:
        if "\\x00" not in item:
            temp_ssid = item.strip().split("SSID: ")[1]
            ssid = uc.str_to_chinese(temp_ssid)
            results.append(ssid)
    return list(set(results))
