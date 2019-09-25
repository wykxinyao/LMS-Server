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


def mount_network(username, password, path, target_path):
    """
    挂载
    :param username: 源系统用户名
    :param password: 源系统密码
    :param path: 源系统路径
    :param target_path: 目标路径
    :return: None
    """
    os.popen("mount -t cifs -o username=" + username + ",password=" + password + " " + path + " " + target_path)


def mount_local():
    """
    本地挂载
    :return:None
    """
    os.popen("mount -t auto /dev/sda1 /mnt/usb")


def mount_list():
    """
    获取当前挂载列表
    :return: list
    """
    temp = os.popen("mount")
    mount = str(temp.read()).split("\n")
    path = []
    for item in mount:
        if "/dev/sda1" in item:
            path.append("/dev/sda1 -> %s" % item.split("/dev/sda1 on ")[1].split(" type")[0])
    return path


def umount(path):
    os.popen("mount -v %s" % path)
