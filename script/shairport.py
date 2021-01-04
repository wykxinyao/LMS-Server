# coding:utf8
# author:Lysio
# python version:2.7

"""
    Dietpi Config Server Copyright 2004-2020 Dreamtech.

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

import utils.service_util as service


def check_status():
    """
    检查shairport-sync服务开启状态
    :return:
    """
    result = service.check_status("shairport-sync")
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
    service.start("shairport-sync")


def stop_service():
    """
    关闭服务
    :return: None
    """
    service.stop("shairport-sync")


def restart_service():
    """
    重启服务
    :return: None
    """
    service.restart("shairport-sync")


def boot_status():
    """
    开机启动状态
    :return:
    """
    result = service.boot_status("shairport-sync")
    if result:
        return True
    else:
        return False


def boot_start():
    """
    设置服务开机启动
    :return: None
    """
    service.boot_start("shairport-sync")


def boot_stop():
    """
    设置服务开机不启动
    :return:None
    """
    service.boot_stop("shairport-sync")
