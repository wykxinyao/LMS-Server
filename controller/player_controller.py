# coding:utf8
# author:Xu YiQing
# python version:2.7

import copy
import urllib

from flask import Blueprint
from flask import request
from flask import jsonify

from lms.server import Server

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
        result = fail_json
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
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/list/all")
def list_all():
    """
    分页查询所有歌曲
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        data = []
        page = int(request.args.get("page"))
        count = int(str(SERVER.request("info total songs ?").strip()))
        songs = SERVER.get_all_songs()
        index = 0
        for _ in songs:
            if index < count:
                if page * 50 <= index < (page + 1) * 50:
                    data.append(songs[index])
            index += 1
        result["songs"] = data
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/list/songs")
def search_songs():
    """
    根据歌曲名搜索歌曲
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        songs = urllib.quote(str(request.args.get("songs")))
        result["songs"] = SERVER.search(songs, mode="songs")
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/list/albums")
def search_albums():
    """
    根据专辑名称查询专辑
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        albums = urllib.quote(str(request.args.get("albums")))
        result["albums"] = SERVER.search(albums, mode="albums")
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/list/artists")
def search_artist():
    """
    根据艺术家名称搜索艺术家
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        artists = urllib.quote(str(request.args.get("artists")))
        result["artists"] = SERVER.search(artists, mode="artists")
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
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
        result = fail_json
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
        result = fail_json
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
        result = fail_json
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
        result = fail_json
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
        result = fail_json
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
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/total/genres")
def total_genres():
    """
    流派总数
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        total = str(SERVER.request("info total genres ?")).strip()
        result["count"] = total
    except Exception, exp:
        result = fail_json
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
        result = fail_json
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
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/find/songs")
def find_songs():
    """
    根据条件查找歌曲
    """
    result = copy.copy(success_json)
    try:
        global SERVER
        album_id = request.args.get("album_id")
        artist_id = request.args.get("artist_id")
        genre_id = request.args.get("genre_id")
        songs = SERVER.find_songs(album_id=album_id, artist_id=artist_id, genre_id=genre_id)
        result["songs"] = songs
    except Exception, exp:
        result = fail_json
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
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@player_controller.route("/current/info")
def get_current_info():
    """
    获得当前播放歌曲的信息
    :return:
    """
    result = copy.copy(success_json)
    try:
        global PLAYER
        data = {
            "album": PLAYER.get_track_album(),
            "artist": PLAYER.get_track_artist(),
            "title": PLAYER.get_track_title(),
            "genre": PLAYER.get_track_genre(),
            "total_time": PLAYER.get_track_duration(),
            "path": PLAYER.get_track_path().replace("%20", " "),
            "current_time": PLAYER.get_time_remaining()
        }
        result["data"] = data
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)
