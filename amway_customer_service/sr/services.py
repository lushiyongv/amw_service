# coding=utf-8
from amway_customer_service.sr.models import SRUserInfo, SRPermissionControl, PERMISSION_TYPE_CHOICES, FOLLOW_UP_TYPE_CHOICES, SRFollowUpType


def get_sr_info_by_pk(sid):
    try:
        return SRUserInfo.objects.get(pk=int(sid))
    except SRUserInfo.DoesNotExist:
        return None


def get_sr_info_sr_id(sr_id):
    try:
        return SRUserInfo.objects.get(sr_id=long(sr_id))
    except SRUserInfo.DoesNotExist:
        return None


def get_sr_permission(sr_info, permission_type):
    kwargs = dict()
    kwargs['permission_type'] = permission_type

    return sr_info.permissions.get(**kwargs)


def get_sr_permission_by_sr_id(sr_id, permission_type):
    sr_info = get_sr_info_sr_id(sr_id)
    if sr_info:
        return get_sr_permission(sr_info, permission_type)
    else:
        return None


def increase_permission_version(sr_user, permission_type):
    sr_permission = get_sr_permission(sr_user, permission_type)
    sr_permission.version += 1
    sr_permission.save()


def get_sr_follow_up_types(sr_info):
    return sr_info.follow_ups.all()


def get_sr_follow_up_type(follow_up_id):
    try:
        return SRFollowUpType.objects.get(pk=int(follow_up_id))
    except SRFollowUpType.DoesNotExist:
        return None


def signup_sr_user_info(sr_id, sr_name, sr_photo, sr_data):
    sr_user_info = SRUserInfo()
    sr_user_info.sr_id = long(sr_id)
    sr_user_info.name = sr_name
    sr_user_info.photo = sr_photo
    sr_user_info.info_data = sr_data
    sr_user_info.save()

    permission_list = list()
    for permission in PERMISSION_TYPE_CHOICES:
        sr_permission = SRPermissionControl()
        sr_permission.permission_type = permission[0]
        sr_permission.permission_name = permission[1]
        sr_permission.version = 0
        sr_permission.sr_user = sr_user_info
        sr_permission.save()
        permission_list.append(sr_permission)

    follow_up_type_list = list()
    for follow_up_type in FOLLOW_UP_TYPE_CHOICES:
        sr_follow_up = SRFollowUpType()
        sr_follow_up.type_id = follow_up_type[0]
        sr_follow_up.type_name = follow_up_type[1]
        sr_follow_up.color = follow_up_type[2]
        sr_follow_up.enabled = True
        sr_follow_up.sr_user = sr_user_info
        sr_follow_up.save()
        follow_up_type_list.append(sr_follow_up)

    return sr_user_info, permission_list, follow_up_type_list


def add_sr_follow_up_type(sr_user, name, color, version):
    if not check_version_on_follow_up_type(sr_user, version):
        return None, False

    sr_follow_up = SRFollowUpType()
    sr_follow_up.type_id = 0
    sr_follow_up.type_name = name
    sr_follow_up.color = color
    sr_follow_up.enabled = True
    sr_follow_up.sr_user = sr_user
    sr_follow_up.save()

    increase_permission_version(sr_user, PERMISSION_TYPE_CHOICES[0][0])

    return sr_follow_up, True


def delete_sr_follow_up_type(sr_user, follow_up_id, version):
    """
    返回 跟进类型，同时返回是否有权限删除
    :param follow_up_id:
    :return:
    """

    sr_follow_up_type = get_sr_follow_up_type(follow_up_id)
    if sr_follow_up_type.sr_user.pk != sr_user.id:
        return None, True, True
    elif not sr_follow_up_type:
        return None, True, True
    elif not can_delete_follow_up_type(sr_follow_up_type):
        return sr_follow_up_type, False, True
    elif not check_version_on_follow_up_type(sr_user, version):
        return sr_follow_up_type, True, False
    else:
        sr_follow_up_type.enabled = False
        sr_follow_up_type.save()

        increase_permission_version(sr_user, PERMISSION_TYPE_CHOICES[0][0])

        return sr_follow_up_type, True, True


def update_sr_follow_up_type(sr_user, follow_up_id, name, color, version):
    sr_follow_up_type = get_sr_follow_up_type(follow_up_id)
    if sr_follow_up_type.sr_user.pk != sr_user.id:
        return None, True, True
    elif not sr_follow_up_type:
        return None, True, True
    elif not can_update_follow_up_type(sr_follow_up_type):
        return sr_follow_up_type, False, True
    elif not check_version_on_follow_up_type(sr_user, version):
        return sr_follow_up_type, True, False
    else:
        sr_follow_up_type.type_name = name
        sr_follow_up_type.color = color
        sr_follow_up_type.save()

        increase_permission_version(sr_user, PERMISSION_TYPE_CHOICES[0][0])

        return sr_follow_up_type, True, True


def can_update_follow_up_type(sr_follow_up_type):
    if sr_follow_up_type.type_id == 100 \
            or sr_follow_up_type.type_id == 101 \
            or sr_follow_up_type.type_id == 102 \
            or sr_follow_up_type.type_id == 103 \
            or sr_follow_up_type.type_id == 104:
        return False
    else:
        return True


def can_delete_follow_up_type(sr_follow_up_type):
    return can_update_follow_up_type(sr_follow_up_type)


def check_version_on_follow_up_type(sr_user_info, version):
    sr_permission = get_sr_permission(sr_user_info, PERMISSION_TYPE_CHOICES[0][0])
    if int(version) == sr_permission.version:
        return True
    else:
        return False