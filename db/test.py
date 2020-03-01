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

from core import DB
import dbutil

db = DB()

conn = db.get_connction()
cursor = conn.cursor()


def insert():
    cursor.execute("insert into track (id,title,album,artist,duration,bitrate,samplesize,samplerate,url) values "
                   "('6','夜曲','叶惠美','周杰伦','666','666','666','666','file://192.168.0.1')")
    cursor.execute("insert into track (id,title,album,artist,duration,bitrate,samplesize,samplerate,url) values "
                   "('7','夜曲','叶惠美','周杰伦','666','666','666','666','file://192.168.0.1')")
    cursor.execute("insert into track (id,title,album,artist,duration,bitrate,samplesize,samplerate,url) values "
                   "('8','夜曲','叶惠美','周杰伦','666','666','666','666','file://192.168.0.1')")
    cursor.execute("insert into track (id,title,album,artist,duration,bitrate,samplesize,samplerate,url) values "
                   "('9','夜曲','叶惠美','周杰伦','666','666','666','666','file://192.168.0.1')")
    cursor.execute("insert into track (id,title,album,artist,duration,bitrate,samplesize,samplerate,url) values "
                   "('10','夜曲','叶惠美','周杰伦','666','666','666','666','file://192.168.0.1')")
    cursor.close()
    conn.commit()
    db.close()

insert()


