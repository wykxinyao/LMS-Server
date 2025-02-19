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
import utils.service_util as service


def check_status():
    """
    检查squeezelite服务开启状态
    :return:
    """
    result = service.check_status("squeezelite")
    if result == "active":
        return True
    elif result == "inactive":
        return False
    else:
        return False


def start_service():
    """
    启动服务
    :return: None
    """
    service.start("squeezelite")


def stop_service():
    """
    关闭服务
    :return: None
    """
    service.stop("squeezelite")


def restart_service():
    """
    重启服务
    :return: None
    """
    service.restart("squeezelite")


def boot_status():
    """
    开机启动状态
    :return:
    """
    result = service.boot_status("squeezelite")
    if result:
        return True
    else:
        return False


def boot_start():
    """
    设置服务开机启动
    :return: None
    """
    service.boot_start("squeezelite")


def boot_stop():
    """
    设置服务开机不启动
    :return:None
    """
    service.boot_stop("squeezelite")


def modify_squeezelite(content):
    """
    修改squeezelite配置文件
    :param content: 修改内容
    :return: None
    """
    copy_success = os.popen('cp /lib/systemd/system/squeezelite.service /lib/systemd/system/squeezelite.service.back')
    if copy_success.read().strip() == "":
        f = open('/lib/systemd/system/squeezelite.service', 'r+')
        f.truncate()
        f.write(
            "[Unit]\r\n" +
            "Description=SqueezeLite (DietPi)\r\n\r\n" +
            "[Service]\r\n" +
            "ExecStart=/usr/bin/squeezelite " +
            content +
            "[Install]\r\n" +
            "WantedBy=multi-user.target\r\n\r\n"
        )
        f.close()
    else:
        pass


def get_squeezelite_list():
    """
    通过squeezelite -l命令获得所有的输出设备供选择
    :return:所有设备的列表
    """
    result = os.popen('squeezelite -l').read()
    temp = result.split('\n')[2:]
    results = []
    for item in temp:
        if item.strip().startswith("hw:CARD"):
            results.append(item)
    return results
