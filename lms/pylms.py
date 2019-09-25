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

import os
import sys
import optparse

try:
    """
    添加运行库
    """
    base_path = os.path.abspath('..')
    sys.path.append(base_path)
    sys.path.append(base_path + os.sep + 'pylms')
    sys.path.append(base_path + os.sep + 'bin')
    sys.path.append(base_path + os.sep + 'docs')
except Exception as e:
    print(e)

from server import Server
from utils.string_util import clean_command
import utils.log_util as log

__revision__ = "$Id$"
__docformat__ = 'restructuredtext en'

# Globals

PROJECT = "PyLMS"
VERSION = "1.00"

VALID_COMMANDS = ["play", "stop", "pause", "unpause", "toggle", "next", "prev",
                  "volume_up", "volume_down", "mute", "unmute", "seek_to",
                  "forward", "rewind", "set_power_state", "set_volume", "show",
                  "display", "infos", "get_ref", "get_uuid", "get_name",
                  "get_ip_address", "get_model", "get_display_type",
                  "get_wifi_signal", "get_mode", "get_time_elapsed",
                  "get_time_remaining", "get_power_state", "get_ir_state",
                  "get_volume", "get_bass", "get_treble", "get_pitch",
                  "get_rate", "get_muting", "get_track_genre",
                  "get_track_artist", "get_track_album", "get_track_title",
                  "get_track_duration", "get_track_remote",
                  "get_track_current_title", "get_track_path", "randomplay",
                  "search", "rescan", "rescanprogress"]

# Option Parsing

parser = optparse.OptionParser(
    usage="%prog or type %prog -h (--help) for help",
    description=__doc__,
    version=PROJECT + " v" + VERSION)
parser.add_option(
    "-s", "--host", dest="host", default="localhost",
    help="Specify Hostname of SqueezeCenter [default: %default]")
parser.add_option(
    "-n", "--port", dest="port", default="9090",
    help="Specify Port of SqueezeCenter [default: %default]")
parser.add_option(
    "-u", "--username", dest="username", default=None,
    help="Specify Authorisation Username")
parser.add_option(
    "-p", "--password", dest="password", default=None,
    help="Specify Authorisation Password")
parser.add_option(
    "-d", "--device", dest="device", default=None,
    help="Specify SqueezePlayer Device MAC Address")
parser.add_option(
    "-i", "--info", dest="info", action="store_true", default=False,
    help="Show Server/Player Information")
parser.add_option(
    "-r", "--raw", dest="raw", action="store_true", default=False,
    help="Output only minimal raw results (useful for scripts)")
parser.add_option(
    "-q", "--quick", dest="quick", action="store_true", default=False,
    help="Perform a quick one-time action (does not query "
         "current device state)")

(options, args) = parser.parse_args()

# 连接服务器

sc = Server(
    hostname=options.host, port=options.port, username=options.username,
    password=options.password)

update_mode = not options.quick

if options.info:
    update_mode = True

try:
    sc.connect(update=update_mode)
except Exception as e:
    log.error(
        "Cannot connect to server (%s:%s)" % (options.host, options.port))
    sys.exit(1)

all_players = sc.players

if options.info:
    log.info("Server Version: %s" % (sc.get_version()))
    for p in all_players:
        log.info(
            "Player: %s | %s | V: %i | M: %s | T: %s | C: %s | W: %s" %
            (p.ref, p.name, p.get_volume(), p.get_mode(), p.get_time_elapsed(),
             p.is_connected, p.get_wifi_signal_strength()))

players = []
if options.device == 'all':
    players = list(all_players)
else:
    sel_player = sc.get_player(options.device)
    if sel_player:
        players.append(sel_player)

if options.device and len(players) == 0:
    log.error("Cannot find player %s" % options.device)
    sys.exit(1)

if not args:
    log.warn("No arguments provided")
    sys.exit(0)

command_map = {}

for c in VALID_COMMANDS:
    cleaned = clean_command(c)
    command_map[cleaned] = c

cmd = clean_command(args[0])

try:
    params = args[1:]
except IndexError:
    params = []

raw_cmd = command_map.get(cmd)

if len(players) == 0:
    # server command
    if cmd in command_map:
        func = getattr(sc, raw_cmd, None)
        try:
            log.info(
                "%s: %s [%s]" % ('server', raw_cmd.upper(), ", ".join(params)))
            result = func(*params)
            if options.raw:
                if result is not None:
                    print(result)
            else:
                if result is None:
                    result = "No Output"
                log.info("[%s] %s" % (raw_cmd, result))
        except ValueError:
            log.error("Invalid parameter")
        except TypeError:
            log.error(
                "Incorrect number of parameters or invalid type parameter")


else:
    for player in players:
        if player is not None:
            if cmd in command_map:
                func = getattr(player, raw_cmd, None)
                try:
                    log.info(
                        "%s: %s [%s]" % (player.name, raw_cmd.upper(),
                                         ", ".join(params)))
                    result = func(*params)
                    if options.raw:
                        if result is not None:
                            print(result)
                    else:
                        if result is None:
                            result = "No Output"
                        log.info("[%s] %s" % (raw_cmd, result))
                except ValueError:
                    log.error("Invalid parameter")
                except TypeError:
                    log.error(
                        "Incorrect number of parameters or invalid "
                        "type parameter")
            else:
                log.error("Invalid command or no device: %s" % cmd)
