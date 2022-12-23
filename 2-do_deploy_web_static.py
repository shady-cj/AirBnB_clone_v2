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
    print(local_archive_path)
    if not os.path.exists(local_archive_path):
        return False

    try:
        with cd('/tmp'):
            file = os.path.basename(local_archive_path) # Gets the filename with extension
            filename = os.path.splitext(file)[0] # Strips the extension off the filename
            put(local_archive_path, file)
            sudo('mkdir -p /data/web_static/releases/{}'.format(filename))
            sudo('tar -xzvf {} -C /data/web_static/releases/{}'.format(file, filename))
            sudo('cp -ru /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}'.format(filename, filename))
            sudo('rm {}'.format(file))
            sudo('rm -r /data/web_static/releases/{}/web_static'.format(filename))
            sudo('rm /data/web_static/current')
            sudo('ln -s /data/web_static/releases/{} /data/web_static/current'.format(filename))
        return True
    except Exception as e:
        print("Error occured", e)
        return False
