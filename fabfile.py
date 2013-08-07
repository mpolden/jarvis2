#!/usr/bin/env python

from fabric.api import env, run, sudo, task
from fabric.context_managers import cd, prefix

env.use_ssh_config = True
home = '~/jarvis2'


@task
def pull_code():
    with cd(home):
        run('git pull --rebase')


@task
def update_dependencies():
    with prefix('workon jarvis2'):
        run('pip install --use-mirrors -r %s/requirements.txt' % (home,))


@task
def restart_server():
    sudo('/etc/init.d/uwsgi restart', pty=False)


@task
def restart_client():
    run('pkill -x midori')


@task(default=True)
def deploy(update_deps=False):
    pull_code()
    if update_deps:
        update_dependencies()
    restart_server()
    restart_client()


@task
def full_deploy():
    deploy(True)
