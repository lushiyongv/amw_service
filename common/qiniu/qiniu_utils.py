# -*- coding: utf-8 -*-
from common.qiniu.qiniu_constants import QINIU_BUCKET_NAME_ZUIMEI
from common.qiniu.qiniu_service import QinuiService
from common.util import image_utils
import os


def format_qiniu_article_image_path(prefix, article_id, image_name, width, height, file_ext):
    key = "img/%s/%s/%s_%dx%d.%s" % (prefix, str(article_id), image_name, int(width), int(height), file_ext)
    return key


def format_qiniu_general_image_path(image_path, width, height):
    f = str(image_path)
    dot_last_index = f.rindex('.')

    pre_key = f[0:dot_last_index]
    file_ext = f[dot_last_index:len(f)]

    key = "img/%s_%dx%d%s" % (pre_key, int(width), int(height), file_ext)
    relative_path = "%s_%dx%d%s" % (pre_key, int(width), int(height), file_ext)
    return key, relative_path

def get_relative_path(seed, file_path):
    width, height = image_utils.parse_image_width_height(file_path)
    key, relative_path = format_qiniu_general_image_path(seed, width, height)
    return key, relative_path

def upload_image(seed, file_path):
    qiniu_service = QinuiService(QINIU_BUCKET_NAME_ZUIMEI)
    key, relative_path = get_relative_path(seed, file_path)
    ret, error = qiniu_service.put_file(key, file_path)
    remote_url = qiniu_service.make_public_url(ret['key'])
    if error is not None:
        return None
    else:
        return key, relative_path, remote_url

def dst_file_name(src, seed_name):
    right_index = seed_name.rindex("/") + 1
    new_file_name = seed_name[right_index:]

    parent_dir = os.path.dirname(src)
    new_file = os.path.join(parent_dir, new_file_name)
    return new_file