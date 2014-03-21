# coding=utf-8
from amway_customer_service.sr.models import PERMISSION_TYPE_CHOICES
from amway_customer_service.sr.services import signup_sr_user_info, get_sr_follow_up_types, get_sr_info_sr_id, add_sr_follow_up_type, \
    delete_sr_follow_up_type, update_sr_follow_up_type, get_sr_permission
from amway_customer_service.utils.http_util import get_error_dict_with_msg, get_json_response, get_error_dict_with_msg_code
from restless.models import serialize
from restless.views import Endpoint


class SRUserSignupView(Endpoint):
    def post(self, request):
        """
        提交注册新的SR，如果已经注册，返回该SR的 Follow Up type
        :param request:
        :return: 返回 Follow up types json
        """
        sr_id = request.POST.get('id', None)
        sr_name = request.POST.get('name', None)
        sr_photo = request.POST.get('photo', None)
        sr_data = request.POST.get('data', None)

        if not sr_id or not sr_name or not sr_photo or not sr_data:
            return get_error_dict_with_msg('Not enough params')

        sr_user = get_sr_info_sr_id(sr_id)
        if sr_user:
            sr_follow_up_types = get_sr_follow_up_types(sr_user)
        else:
            sr_user, sr_permissions, sr_follow_up_types = signup_sr_user_info(sr_id, sr_name, sr_photo, sr_data)
            if not sr_user:
                return get_error_dict_with_msg('SR user signup fail')

        # TODO hard code here, only use the first permission, since only one permission in this version
        sr_permission = sr_permissions[0]
        return get_follow_ups_response(sr_follow_up_types, sr_permission)


class SRUserFollowUpView(Endpoint):
    def get(self, request, sr_id):
        """
        返回该SR所有的 Follow Up type
        :param request:
        :param sr_id:
        :return: 返回 Follow up types json
        """
        sr_user = get_sr_info_sr_id(sr_id)
        if sr_user:
            sr_follow_up_types = get_sr_follow_up_types(sr_user)
        else:
            return get_error_dict_with_msg('SR user is not existed')

        sr_permission = get_sr_permission(sr_user, PERMISSION_TYPE_CHOICES[0][0])
        return get_follow_ups_response(sr_follow_up_types, sr_permission)


class SRUserAddFollowUpView(Endpoint):
    def post(self, request, sr_id):
        """
        增加跟进类型
        :param request:
        :param sr_id:
        """

        type_name = request.POST.get('name', None)
        color = request.POST.get('color', None)
        version = request.POST.get('ver', None)

        if not sr_id or not type_name or not color or not version:
            return get_error_dict_with_msg('Not enough params')

        color_rgba = color.split(',')
        if len(color_rgba) != 4:
            return get_error_dict_with_msg('Color format is invalid')

        sr_user = get_sr_info_sr_id(sr_id)
        if not sr_user:
            return get_error_dict_with_msg('No such sr user')

        sr_follow_up, valid_ver = add_sr_follow_up_type(sr_user, type_name, color, version)
        if not valid_ver:
            return get_error_dict_with_msg_code('Version is not meet', 102)
        else:
            # TODO hard code here, only use the first permission, since only one permission in this version
            sr_permission = get_sr_permission(sr_user, PERMISSION_TYPE_CHOICES[0][0])
            return get_follow_ups_response([serialize(sr_follow_up, exclude=['sr_user'])], sr_permission)


class SRUserDeleteFollowUpView(Endpoint):
    def post(self, request, sr_id, follow_up_id):
        """
        增加跟进类型
        :param request:
        :param sr_id:
        """
        version = request.POST.get('ver', None)

        if not sr_id or not follow_up_id or not version:
            return get_error_dict_with_msg('Not enough params')

        sr_user = get_sr_info_sr_id(sr_id)
        if not sr_user:
            return get_error_dict_with_msg('No such sr user')

        sr_follow_up, can_delete, valid_ver = delete_sr_follow_up_type(sr_user, follow_up_id, version)

        if not sr_follow_up:
            return get_error_dict_with_msg_code('No such follow up', 100)
        elif not can_delete:
            return get_error_dict_with_msg_code('No rights to delete as design', 101)
        elif not valid_ver:
            return get_error_dict_with_msg_code('Version is not meet', 102)
        else:
            # TODO hard code here, only use the first permission, since only one permission in this version
            sr_permission = get_sr_permission(sr_user, PERMISSION_TYPE_CHOICES[0][0])
            return get_follow_ups_response([serialize(sr_follow_up, exclude=['sr_user'])], sr_permission)


class SRUserUpdateFollowUpView(Endpoint):
    def post(self, request, sr_id, follow_up_id):
        """
        增加跟进类型
        :param request:
        :param sr_id:
        """
        version = request.POST.get('ver', None)
        type_name = request.POST.get('name', None)
        color = request.POST.get('color', None)

        if not sr_id or not follow_up_id or not type_name or not color or not version:
            return get_error_dict_with_msg('Not enough params')

        color_rgba = color.split(',')
        if len(color_rgba) != 4:
            return get_error_dict_with_msg('Color format is invalid')

        sr_user = get_sr_info_sr_id(sr_id)
        if not sr_user:
            return get_error_dict_with_msg('No such sr user')

        sr_follow_up, can_update, valid_ver = update_sr_follow_up_type(sr_user, follow_up_id, type_name, color, version)

        if not sr_follow_up:
            return get_error_dict_with_msg_code('No such follow up', 100)
        elif not can_update:
            return get_error_dict_with_msg_code('No rights to delete as design', 101)
        elif not valid_ver:
            return get_error_dict_with_msg_code('Version is not meet', 102)
        else:
            # TODO hard code here, only use the first permission, since only one permission in this version
            sr_permission = get_sr_permission(sr_user, PERMISSION_TYPE_CHOICES[0][0])
            return get_follow_ups_response([serialize(sr_follow_up, exclude=['sr_user'])], sr_permission)


def get_follow_ups_response(sr_follow_up_types, sr_permission):
    follow_up_array = serialize(sr_follow_up_types, exclude=['sr_user'])

    follow_up_dict = dict()
    follow_up_dict['follow_ups'] = follow_up_array
    follow_up_dict['permission'] = serialize(sr_permission, exclude=['sr_user'])

    return get_json_response(follow_up_dict)