#!/usr/bin/env python
# coding:utf-8

import telnetlib
import urllib
from player import Player


class Server(object):
    """
    Server
    """

    def __init__(
            self,
            hostname="localhost",
            port=9090,
            username="",
            password="",
            charset="utf8"):

        """
        Constructor
        """
        self.debug = False
        self.logger = None
        self.telnet = None
        self.logged_in = False
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.version = ""
        self.player_count = 0
        self.players = []
        self.charset = charset
        self.all_songs = []

    def connect(self, update=True):
        """
        Connect
        """
        self.telnet_connect()
        self.login()
        self.get_players(update=update)

    def disconnect(self):
        self.telnet.close()

    def telnet_connect(self):
        """
        Telnet Connect
        """
        self.telnet = telnetlib.Telnet(self.hostname, self.port)

    def login(self):
        """
        Login
        """
        result = self.request("login %s %s" % (self.username, self.password))
        self.logged_in = (result == "******")

    def request(self, command_string, preserve_encoding=False):
        """
        Request
        """
        global command_string_quoted
        self.telnet.write(self.__encode(command_string + "\n"))
        response = self.telnet.read_until(self.__encode("\n"))[:-1]
        if not preserve_encoding:
            response = self.__decode(self.__unquote(response))
        else:
            command_string_quoted = \
                command_string[0:command_string.find(':')] + \
                command_string[command_string.find(':'):].replace(
                    ':', self.__quote(':'))
        start = command_string.split(" ")[0]
        if start in ["songinfo", "trackstat", "albums", "songs", "artists",
                     "rescan", "rescanprogress"]:
            if not preserve_encoding:
                result = response[len(command_string) + 1:]
            else:
                result = response[len(command_string_quoted) + 1:]
        else:
            if not preserve_encoding:
                result = response[len(command_string) - 1:]
            else:
                result = response[len(command_string_quoted) - 1:]
        return result

    def request_with_results(self, command_string, preserve_encoding=False):
        """
        Request with results
        Return tuple (count, results, error_occurred)
        """
        try:
            # init
            quotedColon = urllib.quote(':')
            # request command string
            resultStr = ' ' + self.request(command_string, True)
            # get number of results
            count = 0
            if resultStr.rfind('count%s' % quotedColon) >= 0:
                count = int(resultStr[resultStr.rfind(
                    'count%s' % quotedColon):].replace(
                    'count%s' % quotedColon, ''))
            # remove number of results from result string and cut
            # result string by "id:"
            idIsSep = True
            if resultStr.find(' id%s' % quotedColon) < 0:
                idIsSep = False
            if resultStr.find('count') >= 0:
                resultStr = resultStr[:resultStr.rfind('count') - 1]
            results = resultStr.split(' id%s' % quotedColon)

            output = []
            for result in results:
                result = result.strip()
                if len(result) > 0:
                    if idIsSep:
                        result = 'id%s%s' % (quotedColon, result)
                    subResults = result.split(' ')
                    item = {}
                    for subResult in subResults:
                        key, value = subResult.split(quotedColon, 1)
                        if not preserve_encoding:
                            item[urllib.unquote(key)] = self.__unquote(value)
                        else:
                            item[key] = value
                    output.append(item)
            return count, output, False
        except Exception as e:
            print e
            return 0, [], True

    def get_players(self, update=True):
        """
        Get Players
        """
        self.players = []
        player_count = self.get_player_count()
        for i in range(player_count):
            player = Player(server=self, index=i - 1, update=update)
            self.players.append(player)
        return self.players

    def get_player(self, ref=None):
        """
        Get Player
        """
        if isinstance(ref, str):
            ref = self.__decode(ref)
        ref = ref.lower()
        if ref:
            for player in self.players:
                player_name = player.name.lower()
                player_ref = player.ref.lower()
                if ref == player_ref or ref in player_name:
                    return player

    def get_version(self):
        """
        Get Version
        """
        self.version = self.request("version ?")
        return self.version

    def get_player_count(self):
        """
        Get Number Of Players
        """
        self.player_count = self.request("player count ?")
        return int(self.player_count)

    def search(self, term, mode='albums'):
        """
        Search term in database
        """
        if mode == 'albums':
            return self.request_with_results(
                "albums 0 9999999 tags:%s search:%s" % ("l", term))
        elif mode == 'songs':
            return self.request_with_results(
                "songs 0 9999999 tags:%s search:%s" % ("", term))
        elif mode == 'artists':
            return self.request_with_results(
                "artists 0 9999999 search:%s" % term)

    def get_all_albums(self):
        return self.request_with_results("albums 0 9999999")

    def rescan(self, mode='fast'):
        """
        Rescan library
        Mode can be 'fast' for update changes on library, 'full' for
        complete library scan and 'playlists' for playlists scan only
        """
        is_scanning = True
        try:
            is_scanning = bool(self.request("rescan ?"))
        except Exception as e:
            print e
            pass

        if not is_scanning:
            if mode == 'fast':
                return self.request("rescan")
            elif mode == 'full':
                return self.request("wipecache")
            elif mode == 'playlists':
                return self.request("rescan playlists")
        else:
            return ""

    def rescanprogress(self):
        """
        Return current rescan progress
        """
        return self.request_with_results("rescanprogress")

    def get_path(self, track_id):
        """
        根据歌曲ID获得歌曲路径
        :param track_id:
        :return:
        """
        response = self.request("songinfo 0 100 track_id:%s tags:u" % track_id)
        path = response.split("url:")[1].replace("%20", " ")
        return path

    def get_song_detail(self, track_id):
        """
        根据歌曲ID获得歌曲详细
        :param track_id:
        :return:
        """
        response = str(self.request("songinfo 0 100 track_id:%s tags:u,I,r,T" % track_id))
        data = {"samplesize": response.split(" samplesize:")[1].split(" bitrate:")[0]+"bits",
                "bitrate": response.split(" bitrate:")[1].split(" VBR ")[0],
                "samplerate": response.split(" samplerate:")[1]}
        return data

    def find_songs(self, track_id, album_id, artist_id, genre_id):
        """
        find songs
        """
        base_command = "songs 0 9999999"
        if track_id is not None:
            base_command += " track_id:%s" % track_id
        if album_id is not None:
            base_command += " album_id:%s" % album_id
        if artist_id is not None:
            base_command += " artist_id:%s" % artist_id
        if genre_id is not None:
            base_command += " genre_id:%s" % genre_id
        print base_command
        response = str(self.request(base_command))
        temp = response.split("id:")[1:]
        data = []
        for info in temp:
            song = {}
            string = info.decode("utf-8")
            song_id = string.split(" title:")[0]
            title = string.split(" genre:")[0].split("title:")[1]
            genre = string.split(" artist:")[0].split("genre:")[1]
            artist = string.split(" album:")[0].split("artist:")[1]
            album = string.split(" duration:")[0].split("album:")[1]
            duration = string.split("duration:")[1].strip()
            song["song_id"] = song_id
            song["title"] = title
            song["genre"] = genre
            song["artist"] = artist
            song["album"] = album
            song["duration"] = duration
            data.append(song)
        return data

    def get_all_songs(self):
        """
        Return all songs
        """
        response = str(self.request("songs 0 9999999"))
        temp = response.split("id:")[1:]
        for info in temp:
            song = {}
            string = info.decode("utf-8")
            song_id = string.split(" title:")[0]
            title = string.split(" genre:")[0].split("title:")[1]
            genre = string.split(" artist:")[0].split("genre:")[1]
            artist = string.split(" album:")[0].split("artist:")[1]
            album = string.split(" duration:")[0].split("album:")[1]
            duration = string.split("duration:")[1].strip()
            song["song_id"] = song_id
            song["title"] = title
            song["genre"] = genre
            song["artist"] = artist
            song["album"] = album
            song["duration"] = duration
            self.all_songs.append(song)
        return self.all_songs

    def __encode(self, text):
        return text.encode(self.charset)

    def __decode(self, the_bytes):
        return the_bytes.decode(self.charset)

    def __quote(self, text):
        try:
            import urllib.parse
            return urllib.parse.quote(text, encoding=self.charset)
        except ImportError:
            import urllib
            return urllib.quote(text)

    def __unquote(self, text):
        try:
            import urllib.parse
            return urllib.parse.unquote(text, encoding=self.charset)
        except ImportError:
            import urllib
            return urllib.unquote(text)
