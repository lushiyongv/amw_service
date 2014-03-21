# coding=utf-8
from django.db import models

PERMISSION_TYPE_CHOICES = (
    (1, "跟进信息版本控制"),
)

FOLLOW_UP_TYPE_CHOICES = (
    (100, '初步接触', '00,00,00,00'),
    (101, '购物顾客', '00,00,00,00'),
    (102, '优惠顾客', '00,00,00,00'),
    (103, '合作伙伴', '00,00,00,00'),
    (104, '其它', '00,00,00,00'),
)


class SRUserInfo(models.Model):
    sr_id = models.BigIntegerField(max_length=20, verbose_name='SR ID', unique=True, db_index=True)
    photo = models.URLField(verbose_name='头像')
    name = models.CharField(max_length=50, verbose_name='姓名')
    info_data = models.TextField(verbose_name='SR用户信息', default='')

    class Meta:
        db_table = 'sr_user_info'
        verbose_name = 'SR信息'
        verbose_name_plural = 'SR信息'

    def __unicode__(self):
        return u'%s' % self.name


class SRFollowUpType(models.Model):
    type_id = models.SmallIntegerField(max_length=5, verbose_name='跟进进度类型')
    type_name = models.CharField(max_length=50, verbose_name='跟进进度类型')
    color = models.CharField(max_length=20, verbose_name='RGBA，颜色，逗号分隔')
    enabled = models.BooleanField(default=True, verbose_name='可用')
    sr_user = models.ForeignKey(SRUserInfo, related_name='follow_ups', verbose_name='SR')

    class Meta:
        db_table = 'sr_follow_up_type'
        verbose_name = 'SR跟进进度类型'
        verbose_name_plural = 'SR跟进进度类型'

    def __unicode__(self):
        return u'%s' % self.type


class SRPermissionControl(models.Model):
    permission_name = models.CharField(max_length=50, verbose_name='类型名称')
    permission_type = models.IntegerField(choices=PERMISSION_TYPE_CHOICES, verbose_name='类型ID')
    version = models.IntegerField(verbose_name='当前版本')
    sr_user = models.ForeignKey(SRUserInfo, related_name='permissions', verbose_name='SR')

    class Meta:
        db_table = 'sr_user_permission'
        verbose_name = 'SR操作权限控制'
        verbose_name_plural = 'SR操作权限控制'

    def __unicode__(self):
        return u'%s' % self.permission_name