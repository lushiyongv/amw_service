# -*- coding:utf-8 -*-
from fabric.api import *

env.hosts = ['110.75.189.29']

def update_and_restart():
    env.user = "root"
    env.password = "ourbrixd321"
    with cd('/home/wwwroot/www.brixd.com/amway.brixd.com/amway_service'):
        run('git pull')
        run('sh restart.sh')

def deploy():
    update_and_restart()