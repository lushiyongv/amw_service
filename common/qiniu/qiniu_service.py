# -*- coding: utf-8 -*-
import sys

import qiniu.io
import qiniu.conf
import qiniu.rs
import qiniu.fop
import qiniu.rsf

qiniu.conf.ACCESS_KEY = "jAPrthgDUCWuBubNrVEM1BRQq9id7zl8bRBKMncf"
qiniu.conf.SECRET_KEY = "QeeuZ_1eq0dtthFyb_a1r9bZd6DBIJRaNOHgsKCt"


class QinuiService(object):
    bucket_name = None
    uptoken = None
    #domain = "http://zuimeia.u.qiniudn.com/"
    domain = "zuimeia.u.qiniudn.com"

    def __init__(self, a_bucket_name):
        self.bucket_name = a_bucket_name
        policy = qiniu.rs.PutPolicy(self.bucket_name)
        self.uptoken = policy.token()

    def make_private_url(self, key):
        """ 生成私有下载链接 """

        key = QinuiService._format_key(key)

        base_url = qiniu.rs.make_base_url(self.domain, key)
        policy = qiniu.rs.GetPolicy()
        private_url = policy.make_request(base_url)
        return private_url

    def make_public_url(self, key):
        """生成公有远程链接"""
        key = QinuiService._format_key(key)
        url = qiniu.rs.make_base_url(self.domain, key)
        return url

    def put_file(self, key, local_file_abs_path):
        """ 上传文件的过程 """

        key = QinuiService._format_key(key)

        # 尝试删除, 如果存在
        qiniu.rs.Client().delete(self.bucket_name, key)

        # 上传到七牛
        ret, err = qiniu.io.put_file(self.uptoken, key, local_file_abs_path)
        if err is not None:
            sys.stderr.write('error: %s ' % err)

        return ret, err

    def stat(self, key):
        """ 查看上传文件的内容 """

        key = QinuiService._format_key(key)

        ret, err = qiniu.rs.Client().stat(self.bucket_name, key)
        if err is not None:
            sys.stderr.write('error: %s ' % err)
            return
        print ret,

    def copy(self, key_from, key_to):
        """ 复制文件 """

        # 初始化, 如果要拷贝的文件存在，先删除
        key_from = QinuiService._format_key(key_from)
        key_to = QinuiService._format_key(key_to)

        qiniu.rs.Client().delete(self.bucket_name, key_to)

        ret, err = qiniu.rs.Client().copy(self.bucket_name, key_from, self.bucket_name, key_to)
        if err is not None:
            sys.stderr.write('error: %s ' % err)
            return

        stat, err = qiniu.rs.Client().stat(self.bucket_name, key_to)
        if err is not None:
            sys.stderr.write('error: %s ' % err)
            return
        print 'new file:', stat,

    def move(self, key_from, key_to):
        """ 移动文件 """

        key_from = QinuiService._format_key(key_from)
        key_to = QinuiService._format_key(key_to)

        # 初始化, 如果要挪去的位置存在文件，先删除
        qiniu.rs.Client().delete(self.bucket_name, key_to)

        ret, err = qiniu.rs.Client().move(self.bucket_name, key_from, self.bucket_name, key_to)
        if err is not None:
            sys.stderr.write('error: %s ' % err)
            return

        # 查看文件是否移动成功
        ret, err = qiniu.rs.Client().stat(self.bucket_name, key_to)
        if err is not None:
            sys.stderr.write('error: %s ' % err)
            return

        # 查看文件是否被删除
        ret, err = qiniu.rs.Client().stat(self.bucket_name, key_from)
        if err is None:
            sys.stderr.write('error: %s ' % "删除失败")
            return

    def delete(self, key):
        """ 删除文件 """
        key = QinuiService._format_key(key)

        ret, err = qiniu.rs.Client().delete(self.bucket_name, key)
        if err is not None:
            sys.stderr.write('error: %s ' % err)
            return

        ret, err = qiniu.rs.Client().stat(self.bucket_name, key)
        if err is None:
            sys.stderr.write('error: %s ' % "删除失败")
            return

    @staticmethod
    def _format_key(key):
        if len(key) > 0 and key.startswith("/"):
            key = key[1:len(key)]

        return key