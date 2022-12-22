#!/usr/bin/python3
"""
Using Fabric to run commands locally..
Fabric runs the tar command to archive the web_static directory
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Archives the web_static directory
    """
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz"\
        .format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    command = local('tar -cvzf {} web_static/'.format(archive_name))
    if command.failed:
        return None
    return os.path.abspath(archive_name)
