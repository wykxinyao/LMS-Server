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

import datetime

INFO_LEVEL = "INFO"
ERROR_LEVEL = "ERROR"
WARN_LEVEL = "WARN"


def log(msg, level):
    """
    打印日志
    :param msg:日志信息
    :param level: 日志级别
    :return:None
    """
    print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] [" + level + "] " + msg


def info(msg):
    """
    打印日志
    :param msg:日志信息
    :return:None
    """
    print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] [" + INFO_LEVEL + "] " + msg


def warn(msg):
    """
    打印警告日志
    :param msg:日志信息
    :return:None
    """
    print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] [" + WARN_LEVEL + "] " + msg


def error(msg):
    """
    打印错误日志
    :param msg:日志信息
    :return:None
    """
    print "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] [" + ERROR_LEVEL + "] " + msg
