# -*- coding:utf-8 -*-
import PIL.Image


def parse_image_width_height(image_file):
    """
    @param image_file: 图片文件
    """
    img = PIL.Image.open(image_file)
    width, height = img.size

    return width, height