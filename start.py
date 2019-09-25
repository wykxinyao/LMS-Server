# coding:utf8
# author:Xu YiQing
# python version:2.7

"""
Opera Server Copyright 2004-2019 Dreamtech.
"""

import os
import sys

try:
    """
    Add packages that runs dependencies
    """
    base_path = os.path.abspath('.')
    sys.path.append(base_path)
    sys.path.append(base_path + os.sep + 'click')
    sys.path.append(base_path + os.sep + 'config')
    sys.path.append(base_path + os.sep + 'controller')
    sys.path.append(base_path + os.sep + 'flask')
    sys.path.append(base_path + os.sep + 'http')
    sys.path.append(base_path + os.sep + 'itsdangerous')
    sys.path.append(base_path + os.sep + 'jinja2')
    sys.path.append(base_path + os.sep + 'lms')
    sys.path.append(base_path + os.sep + 'markupsafe')
    sys.path.append(base_path + os.sep + 'script')
    sys.path.append(base_path + os.sep + 'utils')
    sys.path.append(base_path + os.sep + 'werkzeug')
except Exception as e:
    print e

from config import config

from flask import Flask

from controller.config_controller import config_controller
from controller.player_controller import player_controller

# handling coding problems
reload(sys)
sys.setdefaultencoding('utf8')

# We use flask framework
app = Flask(__name__)

# config controller
app.register_blueprint(config_controller, url_prefix="/config")
# player controller
app.register_blueprint(player_controller, url_prefix="/player")

# start the server
if __name__ == '__main__':
    app.run(host=config.BIND_IP, port=config.SERVER_PORT, debug=False)
