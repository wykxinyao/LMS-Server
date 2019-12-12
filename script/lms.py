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

import utils.service_util as service


def check_status():
    """
    检查logitechmediaserver服务开启状态
    :return:
    """
    result = service.check_status("logitechmediaserver")
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
    service.start("logitechmediaserver")


def stop_service():
    """
    关闭服务
    :return: None
    """
    service.stop("logitechmediaserver")


def restart_service():
    """
    重启服务
    :return: None
    """
    service.restart("logitechmediaserver")


def boot_status():
    """
    开机启动状态
    :return:
    """
    result = service.boot_status("logitechmediaserver")
    if result:
        return True
    else:
        return False


def boot_start():
    """
    设置服务开机启动
    :return: None
    """
    service.boot_start("logitechmediaserver")


def boot_stop():
    """
    设置服务开机不启动
    :return:None
    """
    service.boot_stop("logitechmediaserver")
