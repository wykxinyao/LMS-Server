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

reload(sys)
sys.setdefaultencoding('utf8')

try:
    """
    添加运行库
    """
    base_path = os.path.abspath('.')
    sys.path.append(base_path)
    sys.path.append(base_path + os.sep + 'config')
    sys.path.append(base_path + os.sep + 'http')
    sys.path.append(base_path + os.sep + 'script')
    sys.path.append(base_path + os.sep + 'utils')
    sys.path.append(base_path + os.sep + 'lms')
except Exception as e:
    print e

from lms.server import Server
from lms.player import Player

server = Server(hostname="192.168.0.104", port=9090)
server.connect()
player = server.get_player("Opera")

print server.get_all_songs()[15]
print player.request("titles 0 1000")
# print player.request("musicfolder 0 100 folder_id:270")
# print server.request("songinfo 0 10000 track_id:241")
