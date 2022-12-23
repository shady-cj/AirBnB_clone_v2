#!/usr/bin/python3
"""
Using Fabric to run commands remotely..
Fabric deploys an archive to remote hosts
"""
from fabric.api import local, env, execute, run, cd, put, sudo
from datetime import datetime
import os


env.hosts = [
            '54.209.240.136',
            '100.24.237.186'
        ]
env.user = 'ubuntu'


def do_deploy(archive_path=None):
    """
    Deploys an archive to a remote hosts
    """
    local_archive_path = os.path.abspath(archive_path)
    if not os.path.exists(local_archive_path):
        return False

    try:
        with cd('/tmp'):
            # Gets the filename with extension
            file = os.path.basename(local_archive_path)

            # Strips the extension off the filename
            filename = os.path.splitext(file)[0]
            put(local_archive_path, file)
            sudo('mkdir -p /data/web_static/releases/{}'.format(filename))
            sudo('tar -xzf {} -C /data/web_static/releases/{}'
                 .format(file, filename))
            sudo('cp -ru /data/web_static/releases/{}/web_static/* \
/data/web_static/releases/{}'.format(filename, filename))
            sudo('rm {}'.format(file))
            sudo('rm -rf /data/web_static/releases/{}/web_static'
                 .format(filename))
            sudo('rm -rf /data/web_static/current')
            sudo('ln -s /data/web_static/releases/{} /data/web_static/current'
                 .format(filename))
        return True
    except Exception as e:
        return False
