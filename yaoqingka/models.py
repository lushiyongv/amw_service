# -*- coding:utf-8 -*-
from colorful.fields import RGBColorField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
import shutil
import random
import time
from tinymce.models import HTMLField

from common.qiniu.qiniu_constants import QINIU_IMAGE_DOMAIN
#import caching.base
from common.qiniu import qiniu_utils

def rename_file(filename):
    parts = filename.split(".")
    new_name = time.strftime('%Y%m%d%H%M%S')
    new_name += '%d' % random.randint(10000, 99999)
    new_name += '.%s' % parts[-1]

    return new_name

def card_image_path(instance, filename):
    name = rename_file(filename)
    return 'amway_service/invit_card/%s' % name

class InviteCard(models.Model):
    title = models.CharField(max_length=30, blank=True)  # 标题
    addressor = models.CharField(max_length=50, blank=True)  # 发件人
    recipient = models.CharField(max_length=50, blank=True)  # 收件人
    content = HTMLField(max_length=500, blank=True)  # 内容
    order = models.IntegerField(max_length=10, default=0)  # 顺序
    card_image = models.ImageField(upload_to=card_image_path, default="")
    POSITION = (
        ('top', '顶部'),
        ('bottom', '底部'),
    )
    word_postion = models.CharField(max_length=10,
                                choices=POSITION,
                                default='top')
    # word_postion = models.IntegerField(max_length=5, default=1)  #1 上  2 下
    word_color = RGBColorField()
    can_show = models.BooleanField(default=True)
    author = models.ForeignKey(User,  blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def categories(self):
        return ', '.join([obj.title for obj in self.category.all()])

    @property
    def get_card_image(self):
        # if self.card_image.find(QINIU_IMAGE_DOMAIN) > -1:
        #     return self.card_image
        # else:
        #     result = "%s%s%s" % (QINIU_IMAGE_DOMAIN, "img/", self.card_image)
        #     return result
        result = "%s%s%s" % (QINIU_IMAGE_DOMAIN, "img/", self.card_image)
        return result

    @property
    def get_all_tags(self):
        return self.category.all()

    def __unicode__(self):
        # return u'id = %d, title:%s, publication_date:%s' % (self.id, self.title, self.publication_date)
        return u'%s|%d' % (self.title, self.id)

    def save(self, force_insert=False, force_update=False, commit=True):

        if self.pk is not None:  # 修改
            orig = InviteCard.objects.get(pk=self.pk)
            super(InviteCard, self).save()
            if orig.card_image != self.card_image:
                key, relative_path_cover, remote_url  = qiniu_utils.upload_image(self.card_image, self.card_image.path)
                dst_cover_file = qiniu_utils.dst_file_name(self.card_image.path, relative_path_cover)
                shutil.copyfile(self.card_image.path, dst_cover_file)
                self.card_image = relative_path_cover

            super(InviteCard, self).save()

        else:  # 新建
            super(InviteCard, self).save()
            self.order = self.id * 2 - 1

            key_cover, relative_path_cover, remote_url = qiniu_utils.upload_image(self.card_image, self.card_image.path)
            dst_cover_file = qiniu_utils.dst_file_name(self.card_image.path, relative_path_cover)
            shutil.copyfile(self.card_image.path, dst_cover_file)
            self.card_image = relative_path_cover

            super(InviteCard, self).save()

    class Meta:
        ordering = ['-order']
        verbose_name = '邀请卡'
        verbose_name_plural = '【邀请卡管理】邀请卡'