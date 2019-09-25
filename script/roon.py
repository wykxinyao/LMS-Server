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

import utils.log_util as log
import utils.service_util as service


def check_status():
    """
    检查roonbridge服务开启状态
    :return:
    """
    result = service.check_status("roonbridge")
    if result == "active":
        log.log("Service roonbridge is active", log.INFO_LEVEL)
        return True
    elif result == "inactive":
        log.log("Service roonbridge is inactive", log.INFO_LEVEL)
        return False
    else:
        log.log("Service Status Check Error", log.ERROR_LEVEL)
        return False


def start_service():
    """
    启动服务
    :return: None
    """
    service.start("roonbridge")
    log.log("Start Service roonbridge", log.INFO_LEVEL)


def stop_service():
    """
    关闭服务
    :return: None
    """
    service.stop("roonbridge")
    log.log("Stop Service roonbridge", log.INFO_LEVEL)


def restart_service():
    """
    重启服务
    :return: None
    """
    service.restart("roonbridge")
    log.log("Restart Service roonbridge", log.INFO_LEVEL)


def boot_status():
    """
    开机启动状态
    :return:
    """
    result = service.boot_status("roonbridge")
    if result:
        log.log("Service roonbridge Start When Boot", log.INFO_LEVEL)
        return True
    else:
        log.log("Service roonbridge Not Start When Boot", log.INFO_LEVEL)
        return False


def boot_start():
    """
    设置服务开机启动
    :return: None
    """
    service.boot_start("roonbridge")
    log.log("Set Service roonbridge Start When Boot", log.INFO_LEVEL)


def boot_stop():
    """
    设置服务开机不启动
    :return:None
    """
    service.boot_stop("roonbridge")
    log.log("Set Service roonbridge Not Start When Boot", log.INFO_LEVEL)
