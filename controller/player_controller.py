# coding:utf8
# author:Xu YiQing
# python version:2.7

import copy
import urllib

from flask import Blueprint
from flask import request
from flask import jsonify

from lms.server import Server

from db import dbutil
from db import core

player_controller = Blueprint('play_controller', __name__)

success_json = {'success': True, 'status': 200}
fail_json = {'success': False, 'status': 500}

SERVER = None
PLAYER = None


@player_controller.route("/connect")
def connect():
    """
    连接到服务器，执行所有操作之前需要执行
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        hostname = request.args.get("hostname")
        port = int(request.args.get("port"))
        SERVER = Server(hostname=hostname, port=port)
        SERVER.connect()
        result["server_version"] = SERVER.get_version()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/disconnect")
def disconnect():
    """
    断开和服务器的连接，执行所有操作之前需要执行
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        SERVER.disconnect()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/list/songs")
def search_songs():
    """
    根据歌曲名搜索歌曲
    """
    result = copy.copy(success_json)
    try:
        db = core.DB()
        connection = db.get_connction()

        name = request.args.get("name")
        page_size = request.args.get("page_size")
        page = request.args.get("page")

        if name is None or name is "":
            result["tracks"] = dbutil.select_track_by_page(connection=connection, page_size=int(page_size),
                                                           page=int(page))
        else:
            name_ = urllib.unquote(name)
            result["tracks"] = dbutil.select_track_by_name(connection=connection, title=str(name_), page_size=int(page_size),
                                                           page=int(page))
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/list/albums")
def search_albums():
    """
    根据专辑名称查询专辑
    """
    result = copy.copy(success_json)
    try:
        db = core.DB()
        connection = db.get_connction()

        name = request.args.get("name")
        page_size = request.args.get("page_size")
        page = request.args.get("page")

        if name is None or name is "":
            result["albums"] = dbutil.select_album_by_page(connection=connection, page_size=int(page_size),
                                                           page=int(page))
        else:
            name_ = urllib.unquote(name)
            result["albums"] = dbutil.select_album_by_name(connection=connection, album=str(name_),
                                                           page_size=int(page_size),
                                                           page=int(page))
    except Exception, exp:
        result = copy.copy(fail_json)
        result["albums"] = exp.message
    return jsonify(result)


@player_controller.route("/list/artists")
def search_artist():
    """
    根据艺术家名称搜索艺术家
    """
    result = copy.copy(success_json)
    try:
        db = core.DB()
        connection = db.get_connction()

        name = request.args.get("name")
        page_size = request.args.get("page_size")
        page = request.args.get("page")

        if name is None or name is "":
            result["artists"] = dbutil.select_artist_by_page(connection=connection, page_size=int(page_size),
                                                             page=int(page))
        else:
            name_ = urllib.unquote(name)
            result["artists"] = dbutil.select_artist_by_name(connection=connection, artist=str(name_),
                                                             page_size=int(page_size), page=int(page))
    except Exception, exp:
        result = copy.copy(fail_json)
        result["artists"] = exp.message
    return jsonify(result)


@player_controller.route("/list/players")
def get_players():
    """
    播放器列表，供用户选择
    """
    result = copy.copy(success_json)
    try:
        global SERVER, PLAYER
        data = {}
        for temp in SERVER.get_players():
            player = str(temp).split("Player: ")[1]
            PLAYER = SERVER.get_player(player)
            data[PLAYER.get_name()] = player
        result["players"] = data
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/set/player")
def set_player():
    """
    选择播放器
    """
    result = copy.copy(success_json)
    try:
        global SERVER, PLAYER
        player = request.args.get("player")
        PLAYER = SERVER.get_player(player)
        result["player_name"] = PLAYER.get_name()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/rescan")
def rescan():
    """
    重新扫描
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        SERVER.rescan()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/rescanprogress")
def rescanprogress():
    """
    重新扫描
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        temp = SERVER.rescan_progress()
        data = temp[1][0]['rescan']
        result['data'] = data
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/play")
def play():
    """
    播放
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        PLAYER.play()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/pause")
def pause():
    """
    暂停
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        PLAYER.pause()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/total/artists")
def total_artists():
    """
    艺术家总数
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        total = str(SERVER.request("info total artists ?")).strip()
        result["count"] = total
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/total/albums")
def total_albums():
    """
    专辑总数
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        total = str(SERVER.request("info total albums ?")).strip()
        result["count"] = total
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/total/songs")
def total_songs():
    """
    歌曲总数
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        total = str(SERVER.request("info total songs ?")).strip()
        result["count"] = total
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/find/songs")
def find_songs():
    """
    根据条件查找歌曲
    """
    result = copy.copy(success_json)
    try:
        db = core.DB()
        connection = db.get_connction()

        track_id = request.args.get("track_id")
        album = request.args.get("album")
        artist = request.args.get("artist")
        page_size = request.args.get("page_size")
        page = request.args.get("page")

        if track_id is not None and track_id is not "":
            result["tracks"] = dbutil.select_track_by_id(connection=connection, id=str(track_id))
        if artist is not None and artist is not "":
            artist_ = urllib.unquote(artist)
            result["tracks"] = dbutil.select_track_by_artist(connection=connection, artist=str(artist_),
                                                             page_size=int(page_size), page=int(page))
        if album is not None and album is not "":
            album_ = urllib.unquote(album)
            result["tracks"] = dbutil.select_track_by_album(connection=connection, album=str(album_),
                                                            page_size=int(page_size), page=int(page))
        if (album is None or album is "") and (artist is None or artist is "") and (
                track_id is None or track_id is ""):
            result["tracks"] = dbutil.select_track_by_page(connection=connection, page_size=int(page_size),
                                                           page=int(page))

    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/play/song")
def play_song():
    """
    根据歌曲ID播放
    :return:
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        global PLAYER
        track_id = request.args.get("track_id")
        PLAYER.playlist_play(SERVER.get_path(track_id))
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/current/info")
def get_current_info():
    """
    获得当前播放歌曲的信息
    :return:
    """
    result = copy.copy(success_json)
    global PLAYER
    try:
        data = {
            "player_id": PLAYER.get_ref(),
            "album": PLAYER.get_track_album(),
            "artist": PLAYER.get_track_artist(),
            "title": PLAYER.get_track_title(),
            "total_time": PLAYER.get_track_duration(),
            "path": PLAYER.get_track_path().replace("%20", " "),
            "current_time": PLAYER.get_time_remaining()
        }
    except Exception:
        data = {
            "player_id": "0",
            "album": "未知",
            "artist": "未知",
            "title": "未知",
            "total_time": "0",
            "path": "/",
            "current_time": "未知"
        }
    result["data"] = data
    return jsonify(result)


@player_controller.route("/set/volume")
def set_volume():
    """
    设置音量
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        volume = request.args.get("volume")
        PLAYER.set_volume(volume)
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/get/volume")
def get_volume():
    """
    获取音量
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        volume = PLAYER.get_volume()
        result["volume"] = volume
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/playlist/add/song")
def playlist_add_song():
    """
    播放列表添加歌曲
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        global SERVER
        track_id = request.args.get("track_id")
        PLAYER.playlist_add(SERVER.get_path(track_id))
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/playlist/delete/song")
def playlist_delete_song():
    """
    播放列表删除歌曲
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        global SERVER
        track_id = request.args.get("track_id")
        PLAYER.playlist_delete(SERVER.get_path(track_id))
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/playlist/clear")
def playlist_clear():
    """
    播放列表清空歌曲
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        PLAYER.playlist_clear()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/playlist/add/album")
def playlist_add_album():
    """
    将某个专辑或艺术家添加到播放列表中
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        album_name = request.args.get("album_name")
        artist_name = request.args.get("artist_name")
        PLAYER.playlist_addalbum(album=album_name, artist=artist_name)
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/playlist/load/album")
def playlist_load_album():
    """
    立即播放某个专辑
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        album_name = request.args.get("album_name")
        artist_name = request.args.get("artist_name")
        PLAYER.playlist_loadalbum(album=album_name, artist=artist_name)
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/play/next")
def play_next():
    """
    播放下一首
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        PLAYER.next()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/play/prev")
def play_prev():
    """
    播放上一首
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        PLAYER.prev()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/playlist/info")
def playlist_info():
    """
    当前播放列表信息
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        data = PLAYER.playlist_get_info()
        for temp in data:
            temp["title"] = str(temp["title"]).encode("utf8")
        result["songs"] = data
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/folder/list")
def get_music_folder():
    """
    查找所有播放文件夹
    :return:
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        folder_id = request.args.get("folder_id")
        if folder_id is None:
            response = SERVER.request_with_results("musicfolder 0 999999 ")[1]
        else:
            response = SERVER.request_with_results("musicfolder 0 999999 folder_id:%s " % folder_id)[1]
        result["data"] = response
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/play/random")
def random_play():
    """
    随机播放（直接替换当前播放列表）
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        mode = request.args.get("mode")
        if "tracks" in mode:
            PLAYER.request("randomplay tracks ")
        if "albums" in mode:
            PLAYER.request("randomplay albums ")
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/play/seek")
def seek_to():
    """
    跳转播放进度
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        second = request.args.get("second")
        PLAYER.seek_to(second)
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/play/mode")
def repeat_mode():
    """
    重复模式
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        mode = int(request.args.get("mode"))
        if mode == 0:
            # 播放一遍
            PLAYER.request("playlist repeat 0 ")
        elif mode == 1:
            # 单曲循环
            PLAYER.request("playlist repeat 1 ")
        elif mode == 2:
            # 列表循环
            PLAYER.request("playlist repeat 2 ")
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/radio/local/list")
def radio_local_list():
    """
    获取本地电台
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        data = []
        response = str(PLAYER.request("local items 0 999 ")).split(" count:")[0]
        result["title"] = response.split("title:")[1].split(" id:")[0]
        temp_id = response.split("id:")[1].split(" name:")[0].strip()
        response = str(PLAYER.request("local items 0 999 item_id:" + temp_id + " ")).split(" count:")[0]
        temp = response.split("id:")[2:]
        temp_data = {}
        for item in temp:
            the_id = item.split(" name:")[0].strip()
            temp_data["item_id"] = the_id
            name = item.split(" name:")[1].split(" type:")[0].strip()
            temp_data["name"] = name
            the_type = item.split(" type:")[1].split(" image:")[0].strip()
            temp_data["type"] = the_type
            image = item.split(" image:")[1].split(" isaudio:")[0].strip()
            temp_data["image"] = image
            is_audio = item.split(" isaudio:")[1].split(" hasitems:")[0].strip()
            temp_data["is_audio"] = is_audio
            has_items = item.split(" hasitems:")[1].strip()
            temp_data["has_items"] = has_items
            item.split(" type")
            data.append(temp_data)
            temp_data = {}
        result["data"] = data
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/radio/local/play")
def radio_local_play():
    """
    播放本地电台
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        item_id = request.args.get("item_id")
        PLAYER.request("local playlist play item_id:" + item_id + " ")
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/radio/music/list")
def radio_music_list():
    """
    获取音乐电台
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        data = []
        item_id = request.args.get("item_id")
        if item_id is None:
            response = str(PLAYER.request("music items 0 999 ")).split(" count:")[0]
        else:
            response = str(PLAYER.request("music items 0 999 item_id:" + item_id + " ")).split(" count:")[0]
        result["title"] = response.split("title:")[1].split(" id:")[0]
        temp = response.split("id:")[1:]
        temp_data = {}
        for item in temp:
            the_id = item.split(" name:")[0].strip()
            temp_data["item_id"] = the_id
            name = item.split(" name:")[1].split(" type:")[0].strip()
            temp_data["name"] = name
            the_type = item.split(" type:")[1].split(" isaudio:")[0].strip()
            temp_data["type"] = the_type
            is_audio = item.split(" isaudio:")[1].split(" hasitems:")[0].strip()
            temp_data["is_audio"] = is_audio
            has_items = item.split(" hasitems:")[1].strip()
            temp_data["has_items"] = has_items
            item.split(" type")
            data.append(temp_data)
            temp_data = {}
        result["data"] = data
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/radio/music/play")
def radio_music_play():
    """
    播放音乐电台
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        item_id = request.args.get("item_id")
        PLAYER.request("music playlist play item_id:" + item_id + " ")
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/db/rescan")
def db_rescan():
    result = copy.copy(success_json)
    try:
        global PLAYER

        db = core.DB()
        conn = db.get_connction()

        dbutil.delete_track(conn)
        dbutil.delete_album(conn)
        dbutil.delete_artist(conn)

        dbutil.insert_tracks(server=SERVER, connection=conn)
        dbutil.insert_albums(server=SERVER, connection=conn)
        dbutil.insert_artist(server=SERVER, connection=conn)

    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)
