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


def insert_tracks(server, connection):
    """
    录入歌曲
    :return: None
    """
    songs = server.get_all_songs()
    cursor = connection.cursor()
    for item in songs:
        cursor.execute(
            "insert into track (id,title,album,artist,duration) "
            "values (?,?,?,?,?)",
            (item['id'], item['title'], item['album'], item['artist']))
        temp = server.get_song_detail(item['id'])
        cursor.execute("update track set bitrate=?,samplesize=?,samplerate=?,url=? where id=?",
                       temp['bitrate'], temp['samplesize'], temp['samplerate'], temp['url'], item['id'])
    cursor.close()
    connection.commit()


def insert_albums(server, connection):
    """
    录入专辑
    :return:
    """
    albums = server.get_all_albums()
    cursor = connection.cursor()
    for item in albums:
        cursor.execute(
            "insert into album (id,name) values (?,?)",
            (item['id'], item['album']))
    cursor.close()
    connection.commit()


def insert_artist(server, connection):
    """
    录入艺术家
    :return:
    """
    artists = server.get_all_artists()
    cursor = connection.cursor()
    for item in artists:
        cursor.execute(
            "insert into artist (id,name) values (?,?)",
            (item['id'], item['artist']))
    cursor.close()
    connection.commit()


def delete_track(connection):
    """
    删除所有歌曲
    :param connection: 连接
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute("delete from track")
    cursor.close()
    connection.commit()


def delete_album(connection):
    """
    删除所有专辑
    :param connection: 连接
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute("delete from album")
    cursor.close()
    connection.commit()


def delete_artist(connection):
    """
    删除所有艺术家
    :param connection: 连接
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute("delete from artist")
    cursor.close()
    connection.commit()


def select_track_by_id(connection, id):
    """
    根据ID查找歌曲
    :param connection: 连接
    :param id: 歌曲ID
    :return: 歌曲列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from track where id=?', id)
    values = cursor.fetchall()
    return pack_track(values)


def select_track_by_page(connection, page_size, page):
    """
    分页查找歌曲
    :param connection: 连接
    :param page_size: 每页大小
    :param page: 第几页
    :return: 歌曲列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from track limit ? offset ?', (page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_track(values)


def select_track_by_name(connection, title, page_size, page):
    """
    搜索歌曲并分页
    :param connection: 连接
    :param title: 歌曲名
    :param page_size: 每页大小
    :param page: 第几页
    :return: 歌曲列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from track where title like \'%' + title + '%\' limit ? offset ?',
                   (page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_track(values)


def select_track_by_album(connection, album, page_size, page):
    """
    根据专辑搜索歌曲并分页
    :param connection: 连接
    :param album: 专辑
    :param page_size: 每页大小
    :param page: 第几页
    :return: 歌曲列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from track where album=? limit ? offset ?',
                   (album, page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_track(values)


def select_track_by_artist(connection, artist, page_size, page):
    """
    根据艺术家搜索歌曲并分页
    :param connection: 连接
    :param artist: 艺术家
    :param page_size: 每页大小
    :param page: 第几页
    :return: 歌曲列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from track where artist=? limit ? offset ?',
                   (artist, page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_track(values)


def select_artist_by_page(connection, page_size, page):
    """
    分页查询艺术家
    :param connection: 连接
    :param page_size: 每页大小
    :param page: 第几页
    :return: 艺术家列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from artist where limit ? offset ?',
                   (page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_artist_album(values)


def select_artist_by_name(connection, artist, page_size, page):
    """
    根据名称搜索艺术家并分页
    :param connection: 连接
    :param artist: 艺术家
    :param page_size: 每页大小
    :param page: 第几页
    :return: 艺术家列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from artist where name like \'%' + artist + '%\' limit ? offset ?',
                   (page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_artist_album(values)


def select_album_by_page(connection, page_size, page):
    """
    分页查询专辑
    :param connection: 连接
    :param page_size: 每页大小
    :param page: 第几页
    :return: 专辑列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from artist where limit ? offset ?',
                   (page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_artist_album(values)


def select_album_by_name(connection, album, page_size, page):
    """
    根据名称搜索专辑并分页
    :param connection: 连接
    :param album: 专辑
    :param page_size: 每页大小
    :param page: 第几页
    :return: 艺术家列表
    """
    cursor = connection.cursor()
    cursor.execute('select * from artist where name like \'%' + album + '%\' limit ? offset ?',
                   (page_size, (page - 1) * page_size))
    values = cursor.fetchall()
    return pack_artist_album(values)


def pack_track(values):
    """
    将查询到歌曲封装成列表
    :param values: cursor.fetchall()的结果
    :return: 封装后的列表
    """
    results = []
    for item in values:
        track = {'id': item[0],
                 'title': unicode(item[1], 'utf-8'),
                 'album': unicode(item[2], 'utf-8'),
                 'artist': unicode(item[3], 'utf-8'),
                 'duration': item[4],
                 'bitrate': item[5],
                 'samplesize': item[6],
                 'samplerate': item[7],
                 'url': unicode(item[8], 'utf-8')}
        results.append(track)
    return results


def pack_artist_album(values):
    """
    将查询到的艺术家和专辑封装成列表
    :param values: cursor.fetchall()的结果
    :return: 封装后的列表
    """
    results = []
    for item in values:
        track = {'id': item[0],
                 'name': unicode(item[1], 'utf-8')}
        results.append(track)
    return results
