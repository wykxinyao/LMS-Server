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

import config.config as config
import utils.service_util as service
import urllib
import urllib2
import os
import time
import script.reboot as sr


def check_status():
    """
    检查networkaudiod服务开启状态
    :return:
    """
    result = service.check_status("update.sh")
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
    service.start("update.sh")


def stop_service():
    """
    关闭服务
    :return: None
    """
    service.stop("update.sh")


def restart_service():
    """
    重启服务
    :return: None
    """
    service.restart("update.sh")


def get_all_version_info():
    """
    获得版本信息
    :return:
    """
    url = config.UPDATE_VERSION_URL
    data = urllib2.urlopen(url).read()
    result = str(data).split("\r\n")
    return result


def get_current_version_info():
    """
    获得当前版本信息
    :return:
    """
    return config.VERSION


def download_file(version):
    """
    下载指定版本
    :param version:
    :return:
    """
    url = str(config.UPDATE_FILE_PREFIX) + version + ".zip"
    urllib.urlretrieve(url, "/root/OperaAudio.zip")


def unzip_file():
    """
    解压文件
    :return:
    """
    command = "nohup unzip -o -d /root /root/OperaAudio.zip && rm /root/OperaAudio.zip"
    os.system(command)


def stop_server_hand():
    """
    手动启动方式停止进程
    :return:
    """
    os.popen("ps -ef | grep 'python start.py' | grep -v grep | awk '{print $2}' | xargs kill -9")


def stop_server_auto():
    """
    自动启动方式停止进程
    :return:
    """
    os.popen("ps -ef | grep 'python /root/OperaAudio/start.py' | grep -v grep | awk '{print $2}' | xargs kill -9")


def start_server():
    """
    启动
    :return:
    """
    os.popen("nohup python /root/OperaAudio/start.py>/root/OperaAudio/log 2>&1 &")


def do_update(version):
    """
    执行更新
    :param version:
    :return:
    """
    download_file(version)
    time.sleep(1)
    unzip_file()
    time.sleep(1)
    sr.reboot()
