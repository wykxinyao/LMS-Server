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


class Song(object):
    def __init__(self, song_id, title, genere, artist, album, duration):
        self.song_id = song_id
        self.title = title
        self.genere = genere
        self.artist = artist
        self.album = album
        self.duration = duration

    def __str__(self):
        return "[id : %s,title : %s,genere : %s,artist : %s,album : %s,duration : %s]" \
              % (self.song_id, self.title, self.genere, self.artist, self.album, self.duration)
