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

import sqlite3
import core

conn = core.DB().get_connction()
cursor = conn.cursor()

# 歌曲表
cursor.execute('create table track('
               'id varchar(20) primary key,'
               'title varchar(100),'
               'album varchar(100),'
               'artist varchar(100),'
               'duration varchar(100),'
               'bitrate varchar(100),'
               'samplesize varchar(100),'
               'samplerate varchar(100),'
               'url varchar(200)'
               ')')

# 专辑表
cursor.execute('create table album('
               'id varchar(20) primary key,'
               'name varchar(100)'
               ')')

# 艺术家
cursor.execute('create table artist('
               'id varchar(20) primary key,'
               'name varchar(100)'
               ')')

# 播放列表
cursor.execute('create table playlist('
               'id integer primary key autoincrement,'
               'name varchar(50)'
               ')')

# 播放列表-歌曲关系表
cursor.execute('create table playlist_track('
               'pid varchar(20),'
               'tid varchar(20)'
               ')')

cursor.close()
conn.close()
