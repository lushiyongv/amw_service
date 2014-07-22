# -*- coding:utf-8 -*-
from fabric.api import *

env.hosts = ['182.92.163.118']

def update_and_restart():
    env.user = "root"
    env.password = "fe478c46"
    with cd('/home/wwwroot/briapp/www/amway_service'):
        run('git pull')
        run('sh restart.sh')

def deploy():
    update_and_restart()