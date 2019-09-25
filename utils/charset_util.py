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


def str_to_chinese(var):
    """
    将双反斜杠字符串转换为中文
    :param var: 字符串
    :return: 中文
    """
    global start2, start3, str1, str2, str3
    not_end = True
    while not_end:
        start1 = var.find("\\x")
        if start1 > -1:
            str1 = var[start1 + 2:start1 + 4]
            start2 = var[start1 + 4:].find("\\x") + start1 + 4
            if start2 > -1:
                str2 = var[start2 + 2:start2 + 4]
                start3 = var[start2 + 4:].find("\\x") + start2 + 4
                if start3 > -1:
                    str3 = var[start3 + 2:start3 + 4]
        else:
            not_end = False
        if start1 > -1 and start2 > -1 and start3 > -1:
            str_all = str1 + str2 + str3
            str_all = str_all.decode('hex')
            str_re = var[start1:start3 + 4]
            var = var.replace(str_re, str_all)
    return var.decode('utf-8')
