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


def check_status(service):
    """
    检查服务状态
    :param service:服务名
    :return: 结果
    """
    command = "service " + service + " status"
    check = os.popen(command)
    flag = check.read()
    if "Active: active (running)" in flag:
        return "active"
    elif "Active: inactive (dead)" in flag:
        return "inactive"
    else:
        print "error"


def start(service):
    """
    开启服务
    :param service: 服务名
    :return: None
    """
    command = "service " + service + " start"
    os.popen(command)


def stop(service):
    """
    停止服务
    :param service:服务名
    :return: None
    """
    command = "service " + service + " stop"
    os.popen(command)


def restart(service):
    """
    重启服务
    :param service: 服务名
    :return: None
    """
    command = "service " + service + " restart"
    os.popen(command)


def boot_start(service):
    """
    设置服务开机自动启动
    :param service:服务名
    :return: None
    """
    command = "systemctl enable " + service
    os.popen(command)


def boot_stop(service):
    """
    设置服务开机不自动启动
    :param service:服务名
    :return: None
    """
    command = "systemctl disable " + service
    os.popen(command)


def boot_status(service):
    """
    检查服务是否开机自动启动
    :param service: 服务名
    :return: Boolean
    """
    command = "systemctl is-enabled " + service
    check = os.popen(command)
    flag = check.read().strip()
    if flag == "enabled" or "enabled" in flag:
        return True
    elif flag == "disabled" or "disabled" in flag:
        return False
    else:
        print False
