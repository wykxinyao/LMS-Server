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
import script.reboot as sr

FILE_PATH = "/etc/rc.local"
# FILE_PATH = "D:\\test.txt"

PREFIX_TEXT = ("#!/bin/sh -e\n" +
               "#\n" +
               "# rc.local\n" +
               "#\n" +
               "# This script is executed at the end of each multiuser runlevel.\n" +
               "# Make sure that the script will \"exit 0\" on success or any other\n" +
               "# value on error.\n" +
               "#\n" +
               "# In order to enable or disable this script just change the execution\n" +
               "# bits.\n" +
               "#\n" +
               "# By default this script does nothing\n" +
               "\n")

SUFFIX_TEXT = ("# Print the IP address\n" +
               "_IP=$(hostname -I) || true\n" +
               "if [ \"$_IP\" ]; then\n" +
               "  printf \"My IP address is %s\\n\" \"$_IP\"\n" +
               "fi\n" +
               "\n" +
               "exit 0\n")


def mount_network(username, password, path):
    """
    挂载
    :param username: 源系统用户名
    :param password: 源系统密码
    :param path: 源系统路径
    :return: None
    """
    os.popen("mkdir /mnt/music/network")
    f = open("/etc/fstab", 'r+')
    data = f.read()
    prefix = data.split("# NETWORK")[0]
    suffix = data.split("# TMPFS")[1]
    start = prefix + "# NETWORK\n" + "#----------------------------------------------------------------\n"
    new = start + "//" + path.strip() + " /mnt/test cifs username=" + username.strip() + ",password=" + password.strip() + ",iocharset=utf8,uid=dietpi,gid=dietpi,file_mode=0770,dir_mode=0770,vers=3.1.1,_netdev,nofail 0 0\n"
    result = new + "#----------------------------------------------------------------\n" + "# TMPFS" + suffix
    f.write(result)
    f.close()
    sr.reboot()


def mount_local():
    """
    本地挂载
    :return:None
    """
    f = open(FILE_PATH, 'r+')
    f.truncate()
    f.write(
        PREFIX_TEXT +
        "/bin/mkdir /mnt/music/sda1;/bin/mount -o iocharset=utf8 -t auto /dev/sda1 /mnt/music/sda1;" +
        "/bin/mkdir /mnt/music/sda2;/bin/mount -o iocharset=utf8 -t auto /dev/sda2 /mnt/music/sda2;" +
        "/bin/mkdir /mnt/music/sdb1;/bin/mount -o iocharset=utf8 -t auto /dev/sdb1 /mnt/music/sdb1;" +
        "/bin/mkdir /mnt/music/sdb2;/bin/mount -o iocharset=utf8 -t auto /dev/sdb2 /mnt/music/sdb2;" +
        "/bin/mkdir /mnt/music/sdc1;/bin/mount -o iocharset=utf8 -t auto /dev/sdc1 /mnt/music/sdc1;" +
        "/bin/mkdir /mnt/music/sdc2;/bin/mount -o iocharset=utf8 -t auto /dev/sdc2 /mnt/music/sdc2;" +
        "/bin/mkdir /mnt/music/sdd1;/bin/mount -o iocharset=utf8 -t auto /dev/sdd1 /mnt/music/sdd1;" +
        "/bin/mkdir /mnt/music/sdd2;/bin/mount -o iocharset=utf8 -t auto /dev/sdd2 /mnt/music/sdd2\n"
        + SUFFIX_TEXT
    )
    f.close()
    sr.reboot()


def mount_list():
    """
    获取当前挂载列表
    :return: list
    """
    path = []
    temp = os.popen("mount")
    mount = str(temp.read()).split("\n")
    for item in mount:
        if "/dev/sda1" in item:
            path.append("/dev/sda1 -> %s" % item.split("/dev/sda1 on ")[1].split(" type")[0])
        if "/dev/sda2" in item:
            path.append("/dev/sda2 -> %s" % item.split("/dev/sda2 on ")[1].split(" type")[0])
        if "/dev/sdb1" in item:
            path.append("/dev/sdb1 -> %s" % item.split("/dev/sdb1 on ")[1].split(" type")[0])
        if "/dev/sdb2" in item:
            path.append("/dev/sdb2 -> %s" % item.split("/dev/sdb2 on ")[1].split(" type")[0])
        if "/dev/sdc1" in item:
            path.append("/dev/sdc1 -> %s" % item.split("/dev/sdc1 on ")[1].split(" type")[0])
        if "/dev/sdc2" in item:
            path.append("/dev/sdc2 -> %s" % item.split("/dev/sdc2 on ")[1].split(" type")[0])
        if "/dev/sdd1" in item:
            path.append("/dev/sdd1 -> %s" % item.split("/dev/sdd1 on ")[1].split(" type")[0])
        if "/dev/sdd2" in item:
            path.append("/dev/sdd2 -> %s" % item.split("/dev/sdd2 on ")[1].split(" type")[0])
    return path


def umount():
    """
    卸载
    :param:
    :return:
    """
    f = open(FILE_PATH, 'r+')
    f.truncate()
    f.write(
        PREFIX_TEXT + SUFFIX_TEXT
    )
    f.close()
    sr.reboot()
