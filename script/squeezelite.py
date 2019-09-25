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
import utils.log_util as log
import utils.service_util as service


def check_status():
    """
    检查squeezelite服务开启状态
    :return:
    """
    result = service.check_status("squeezelite")
    if result == "active":
        log.log("Service Squeezelite is active", log.INFO_LEVEL)
        return True
    elif result == "inactive":
        log.log("Service Squeezelite is inactive", log.INFO_LEVEL)
        return False
    else:
        log.log("Service Status Check Error", log.ERROR_LEVEL)
        return False


def start_service():
    """
    启动服务
    :return: None
    """
    service.start("squeezelite")
    log.log("Start Service Squeezelite", log.INFO_LEVEL)


def stop_service():
    """
    关闭服务
    :return: None
    """
    service.stop("squeezelite")
    log.log("Stop Service Squeezelite", log.INFO_LEVEL)


def restart_service():
    """
    重启服务
    :return: None
    """
    service.restart("squeezelite")
    log.log("Restart Service Squeezelite", log.INFO_LEVEL)


def boot_status():
    """
    开机启动状态
    :return:
    """
    result = service.boot_status("squeezelite")
    if result:
        log.log("Service Squeezelite Start When Boot", log.INFO_LEVEL)
        return True
    else:
        log.log("Service Squeezelite Not Start When Boot", log.INFO_LEVEL)
        return False


def boot_start():
    """
    设置服务开机启动
    :return: None
    """
    service.boot_start("squeezelite")
    log.log("Set Service Squeezelite Start When Boot", log.INFO_LEVEL)


def boot_stop():
    """
    设置服务开机不启动
    :return:None
    """
    service.boot_stop("squeezelite")
    log.log("Set Service Squeezelite Not Start When Boot", log.INFO_LEVEL)


def modify_squeezelite(content):
    """
    修改squeezelite配置文件
    :param content: 修改内容
    :return: None
    """
    copy_success = os.popen('cp /etc/systemd/system/squeezelite.service /etc/systemd/system/squeezelite.service.back')
    if copy_success.read().strip() == "":
        log.log("Backup <squeezelite.service> Success!", log.INFO_LEVEL)
        f = open('/etc/systemd/system/squeezelite.service', 'r+')
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
        log.log("Write New <squeezelite.service> Success!", log.INFO_LEVEL)
    else:
        log.log("Copy Operation Error!", log.ERROR_LEVEL)


def get_squeezelite_list():
    """
    通过squeezelite -l命令获得所有的输出设备供选择
    :return:所有设备的列表
    """
    result = os.popen('squeezelite -l').read()
    temp = result.split('\n')[2:]
    results = []
    for item in temp:
        if "hw:CARD" in item:
            results.append(item)
    return results
