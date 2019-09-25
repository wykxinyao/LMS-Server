# coding:utf8
# author:Xu YiQing
# python version:2.7

import copy

from flask import Blueprint
from flask import jsonify
from flask import request

from script import squeezelite as ss
from script import wifi as sw
from script import lms as sl
from script import roon as sr
from script import naa as sn
from script import halt as sh
from script import reboot as sb
from script import mount as sm
from script import update as su

config_controller = Blueprint('config_controller', __name__)

success_json = {'success': True, 'status': 200}
fail_json = {'success': False, 'status': 500}


@config_controller.route("/modify/squeezelite")
def modify_squeezelite():
    """
    配置Squeezelite
    """
    result = copy.copy(success_json)
    try:
        output = request.args.get("output")
        dsd = request.args.get("dsd")
        prefix = "-o "
        suffix = "  -n 'Opera' -C 3 "
        base = prefix + output + suffix
        if dsd == "DoP":
            content = base + "-D\n"
        elif dsd == "Native":
            content = base + "-D :u32be -p 1\n"
        else:
            content = base + "\n"
        ss.modify_squeezelite(content)
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/list/squeezelite")
def list_squeezelite():
    """
    查询Squeezelite信息
    """
    result = copy.copy(success_json)
    try:
        sq_list = ss.get_squeezelite_list()
        squeezelite_list = []
        for item in sq_list:
            squeezelite_list.append(item)
        result["data"] = squeezelite_list
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/config/wifi")
def config_wifi():
    """
    修改WIFI
    """
    result = copy.copy(success_json)
    try:
        ssid = request.args.get("ssid")
        password = request.args.get("password")
        sw.modify_wifi(ssid, password)
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/list/wifi")
def list_wifi():
    """
    列出可用WIFI
    """
    result = copy.copy(success_json)
    try:
        wifi_list = sw.get_wifi_list()
        data = []
        for item in wifi_list:
            data.append(item)
        result["data"] = data
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/status/squeezelite")
def status_squeezelite():
    """
    查看Squeezelite服务状态
    """
    result = copy.copy(success_json)
    print result
    try:
        service_result = ss.check_status()
        if service_result:
            result["active"] = True
        else:
            result["active"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/start/squeezelite")
def start_squeezelite():
    """
    开启Squeezelite服务
    """
    result = copy.copy(success_json)
    try:
        ss.start_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/stop/squeezelite")
def stop_squeezelite():
    """
    关闭Squeezelite服务
    """
    result = copy.copy(success_json)
    try:
        ss.stop_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/restart/squeezelite")
def restart_squeezelite():
    """
    重启Squeezelite服务
    """
    result = copy.copy(success_json)
    try:
        ss.restart_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_status/squeezelite")
def boot_status_squeezelite():
    """
    查看Squeezelite服务开机启动状态
    """
    result = copy.copy(success_json)
    try:
        boot_result = ss.boot_status()
        if boot_result:
            result["enable"] = True
        else:
            result["enable"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_start/squeezelite")
def boot_start_squeezelite():
    """
    设置Squeezelite服务开机启动
    """
    result = copy.copy(success_json)
    try:
        ss.boot_start()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_stop/squeezelite")
def boot_stop_squeezelite():
    """
    设置Squeezelite服务开机不启动
    """
    result = copy.copy(success_json)
    try:
        ss.boot_stop()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/status/lms")
def status_lms():
    """
    查看LMS服务状态
    """
    result = copy.copy(success_json)
    try:
        service_result = sl.check_status()
        if service_result:
            result["active"] = True
        else:
            result["active"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/start/lms")
def start_lms():
    """
    开启LMS服务
    """
    result = copy.copy(success_json)
    try:
        sl.start_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/stop/lms")
def stop_lms():
    """
    关闭LMS服务
    """
    result = copy.copy(success_json)
    try:
        sl.stop_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/restart/lms")
def restart_lms():
    """
    重启LMS服务
    """
    result = copy.copy(success_json)
    try:
        sl.restart_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_status/lms")
def boot_status_lms():
    """
    查看LMS服务开机启动状态
    """
    result = copy.copy(success_json)
    try:
        boot_result = sl.boot_status()
        if boot_result:
            result["enable"] = True
        else:
            result["enable"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_start/lms")
def boot_start_lms():
    """
    设置LMS服务开机启动
    """
    result = copy.copy(success_json)
    try:
        sl.boot_start()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_stop/squeezelite")
def boot_stop_lms():
    """
    设置LMS服务开机不启动
    """
    result = copy.copy(success_json)
    try:
        sl.boot_stop()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/status/roon")
def status_roon():
    """
    查看Roon服务状态
    """
    result = copy.copy(success_json)
    try:
        service_result = sr.check_status()
        if service_result:
            result["active"] = True
        else:
            result["active"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/start/roon")
def start_roon():
    """
    开启Roon服务
    """
    result = copy.copy(success_json)
    try:
        sr.start_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/stop/roon")
def stop_roon():
    """
    关闭Roon服务
    """
    result = copy.copy(success_json)
    try:
        sr.stop_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/restart/roon")
def restart_roon():
    """
    重启Roon服务
    """
    result = copy.copy(success_json)
    try:
        sr.restart_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_status/roon")
def boot_status_roon():
    """
    查看Roon服务开机启动状态
    """
    result = copy.copy(success_json)
    try:
        boot_result = sr.boot_status()
        if boot_result:
            result["enable"] = True
        else:
            result["enable"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_start/roon")
def boot_start_roon():
    """
    设置Roon服务开机启动
    """
    result = copy.copy(success_json)
    try:
        sr.boot_start()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_stop/roon")
def boot_stop_roon():
    """
    设置Roon服务开机不启动
    """
    result = copy.copy(success_json)
    try:
        sr.boot_stop()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/status/naa")
def status_naa():
    """
    查看naa服务状态
    """
    result = copy.copy(success_json)
    try:
        service_result = sn.check_status()
        if service_result:
            result["active"] = True
        else:
            result["active"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/start/naa")
def start_naa():
    """
    开启naa服务
    """
    result = copy.copy(success_json)
    try:
        sn.start_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/stop/naa")
def stop_naa():
    """
    关闭naa服务
    """
    result = copy.copy(success_json)
    try:
        sn.stop_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/restart/naa")
def restart_naa():
    """
    重启naa服务
    """
    result = copy.copy(success_json)
    try:
        sn.restart_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_status/naa")
def boot_status_naa():
    """
    查看naa服务开机启动状态
    """
    result = copy.copy(success_json)
    try:
        boot_result = sn.boot_status()
        if boot_result:
            result["enable"] = True
        else:
            result["enable"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_start/naa")
def boot_start_naa():
    """
    设置naa服务开机启动
    """
    result = copy.copy(success_json)
    try:
        sn.boot_start()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/boot_stop/naa")
def boot_stop_naa():
    """
    设置naa服务开机不启动
    """
    result = copy.copy(success_json)
    try:
        sn.boot_stop()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/halt")
def halt():
    """
    关机
    """
    result = copy.copy(success_json)
    try:
        sh.halt()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/reboot")
def reboot():
    """
    重启
    """
    result = copy.copy(success_json)
    try:
        sb.reboot()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/umount")
def umount():
    """
    卸载
    """
    result = copy.copy(success_json)
    try:
        path = request.args.get("path")
        sm.umount(path)
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/mount/list")
def mount_list():
    """
    已经挂载的列表
    """
    result = copy.copy(success_json)
    try:
        mount = sm.mount_list()
        result["data"] = mount
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/mount/network")
def network_mount():
    """
    执行网络挂载
    """
    result = copy.copy(success_json)
    try:
        username = request.args.get("username")
        password = request.args.get("password")
        path = request.args.get("path")
        target_path = request.args.get("target_path")
        sm.mount_network(username, password, path, target_path)
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/mount/local")
def local_mount():
    """
    本地挂载
    """
    result = copy.copy(success_json)
    try:
        sm.mount_local()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/status/update")
def status_update():
    """
    查看更新服务状态
    """
    result = copy.copy(success_json)
    try:
        service_result = su.check_status()
        if service_result:
            result["active"] = True
        else:
            result["active"] = False
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/start/update")
def start_update():
    """
    开启更新服务
    """
    result = copy.copy(success_json)
    try:
        su.start_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/stop/update")
def stop_update():
    """
    关闭更新服务
    """
    result = copy.copy(success_json)
    try:
        su.stop_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)


@config_controller.route("/restart/update")
def restart_update():
    """
    重启更新服务
    """
    result = copy.copy(success_json)
    try:
        su.restart_service()
    except Exception, exp:
        result = fail_json
        result["error"] = exp.message
    return jsonify(result)
