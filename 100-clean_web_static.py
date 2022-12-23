#!/usr/bin/python3
"""
Using Fabric to run commands remotely..
Fabric deploys an archive to remote hosts
and clean old archives
"""
from fabric.api import local, env, execute, run, cd, put, sudo, hosts
from datetime import datetime
import os
pack = __import__("1-pack_web_static").do_pack

env.user = 'ubuntu'


@hosts(['54.209.240.136', '100.24.237.186'])
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


def deploy():
    """
    Archive and deploy
    """
    path = execute(pack)
    if path is None:
        return False
    path = path.get('<local-only>')
    ret = execute(do_deploy, path)
    for v in ret.values():
        if not v:
            return False
    return True


def clean_local(number=0):
    """
    Clean archives locally and store
    the removed archives
    """
    number = int(number)
    v = local('ls -t versions', capture=True)
    files = v.splitlines()
    removed_files = []
    if number < 2:
        for file in files[1:]:
            local('rm -f versions/{}'.format(file))
            removed_files.append(file)
    else:
        for file in files[number:]:
            local('rm -f versions/{}'.format(file))
            removed_files.append(file)
    return removed_files


@hosts(['54.209.240.136', '100.24.237.186'])
def clean_remote(removed_files=[]):
    """
    clean directories remotely based on the
    files cleaned locally
    """
    with cd('/data/web_static/releases'):
        for each_files in removed_files:
            filename = os.path.splitext(each_files)[0]
            sudo('rm -rf {}'.format(filename))


def do_clean(number=0):
    """
    Clean up old archives
    """
    local_execute = execute(clean_local, number)
    removed_files = local_execute.get('<local-only>')
    execute(clean_remote, removed_files)
