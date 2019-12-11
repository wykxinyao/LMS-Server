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

server = Server(hostname="192.168.0.101", port=9090)
server.connect()
track_id=186
response = str(server.request("songinfo 0 100 track_id:%s tags:u,I,r,T" % track_id))
data = {"samplesize": response.split(" samplesize:")[1].split(" bitrate:")[0],
        "bitrate": response.split(" bitrate:")[1].split(" VBR ")[0].split("kbps")[0],
        "samplerate": response.split(" samplerate:")[1]}
print data
server.rescan()
player = server.get_player("Opera")
print player.plugins()
print player.request("presets items 0 999 item_id")
print player.request("music items 0 999 item_id:3857457a.0 ")
player.request("local playlist play item_id:6684f6cf.1.0.0 ")
print player.request("music items 0 999 ")
