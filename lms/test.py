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

import sys
import os
import re

reload(sys)
sys.setdefaultencoding('utf8')

try:
    """
    添加运行库
    """
    base_path = os.path.abspath('.')
    sys.path.append(base_path)
    sys.path.append(base_path + os.sep + 'click')
    sys.path.append(base_path + os.sep + 'config')
    sys.path.append(base_path + os.sep + 'controller')
    sys.path.append(base_path + os.sep + 'flask')
    sys.path.append(base_path + os.sep + 'itsdangerous')
    sys.path.append(base_path + os.sep + 'jinja2')
    sys.path.append(base_path + os.sep + 'lms')
    sys.path.append(base_path + os.sep + 'markupsafe')
    sys.path.append(base_path + os.sep + 'script')
    sys.path.append(base_path + os.sep + 'utils')
    sys.path.append(base_path + os.sep + 'werkzeug')
    sys.path.append(base_path + os.sep + 'db')
except Exception as e:
    print e

from lms.server import Server
from lms.player import Player

from db import dbutil
from db import core

import urllib

server = Server(hostname="192.168.1.105", port=9090)
server.connect()

print dbutil.select_track_by_artist(core.DB().get_connction(),"Taylor Swift",3,2)


