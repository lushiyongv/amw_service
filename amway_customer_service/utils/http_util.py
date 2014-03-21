# coding=utf-8


def get_json_response(result_dict):
    return _message_dict(result_dict)


def get_error_dict_with_msg(msg):
    return _error_message_dict(msg, 0)


def get_error_dict_with_msg_code(msg, error_code):
    return _error_message_dict(msg, error_code)


# ===== private methods  ======
def _message_dict(data):
    response_result = dict()
    response_result['result'] = 1
    response_result['reason'] = ''
    response_result['data'] = data
    return response_result


def _error_message_dict(msg, code):
    response_result = dict()
    response_result['result'] = code
    response_result['reason'] = msg
    response_result['data'] = dict()
    return response_result