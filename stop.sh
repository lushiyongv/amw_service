#!/bin/sh
ps -ef | grep 'uwsgi -x uwsgi_config.xml'| grep -v grep | awk '{print $2}' | xargs kill