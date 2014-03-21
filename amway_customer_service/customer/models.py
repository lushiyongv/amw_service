# coding=utf-8
from amway_customer_service.sr.models import SRUserInfo, SRFollowUpType
from django.db import models

BACKUP_ACTION_CHOICES = (
    (0, "新增"),
    (1, "修改"),
    (2, "删除"),
)


class CustomerInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    icon = models.CharField(max_length=200, verbose_name='头像', blank='')
    version = models.IntegerField(max_length=11, verbose_name='版本信息')
    info_data = models.TextField(verbose_name='顾客信息，JSON')
    sr_user = models.ForeignKey(SRUserInfo, verbose_name='SR')
    follow_up_type = models.OneToOneField(SRFollowUpType, verbose_name='跟进信息类型')
    enabled = models.BooleanField(default=True, verbose_name='可用')
    updated_time = models.DateTimeField(verbose_name='更新时间')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'customer_info'
        verbose_name = '顾客信息'
        verbose_name_plural = '顾客信息'

    def __unicode__(self):
        return u'%s' % self.name


class CustomerInfoHistory(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    version = models.IntegerField(max_length=11, verbose_name='版本信息')
    info_data = models.TextField(verbose_name='顾客信息，JSON')
    sr_user = models.ForeignKey(SRUserInfo, verbose_name='SR')
    action = models.IntegerField(choices=BACKUP_ACTION_CHOICES, default=BACKUP_ACTION_CHOICES[0][0], verbose_name='动作类型')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'customer_info_history'
        verbose_name = '顾客历史信息'
        verbose_name_plural = '顾客历史信息'

    def __unicode__(self):
        return u'%s' % self.name