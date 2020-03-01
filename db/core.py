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

TEST_PATH = '../opera.db'
PATH = 'opera.db'


class DB(object):

    def __init__(self):
        self.connection = sqlite3.connect(PATH)
        self.connection.text_factory = str

    def get_connction(self):
        return self.connection

    def get_cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()
