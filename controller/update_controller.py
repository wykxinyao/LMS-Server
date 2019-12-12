# coding:utf8
# author:Xu YiQing
# python version:2.7

import copy

from flask import Blueprint
from flask import jsonify
from flask import request

from script import update as su
from config import config as cc

update_controller = Blueprint('update_controller', __name__)

success_json = {'success': True, 'status': 200}
fail_json = {'success': False, 'status': 500}


@update_controller.route("/list")
def get_update_list():
    """
    得到更新列表
    """
    result = copy.copy(success_json)
    try:
        result["data"] = su.get_all_version_info()
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@update_controller.route("/current")
def get_current_version():
    """
    获取当前版本信息
    """
    result = copy.copy(success_json)
    try:
        result["version"] = cc.VERSION
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)


@update_controller.route("/do")
def do_update():
    result = copy.copy(success_json)
    try:
        version = request.args.get("version")
        data = su.get_all_version_info()
        if version in data:
            su.do_update(version)
        else:
            result = copy.copy(fail_json)
            result["error"] = "version error!"
    except Exception, exp:
        result = copy.copy(fail_json)
        result["error"] = exp.message
    return jsonify(result)
