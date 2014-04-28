__author__ = 'zhangliang'
import urllib2


def get_http_referer(request):
    print request.META
    http_referer = request.META.get('HTTP_REFERER', '/')
    print http_referer
    return http_referer

def is_post_request(request):
    """
    only post request allowed
    """
    if request.method == "POST":
        return True
    else:
        return False


def is_get_request(request):
    """
    only post request allowed
    """
    if request.method == "GET":
        return True
    else:
        return False


def get_request(url):
    #return urllib2.urlopen(url).read()
    response = urllib2.urlopen(url)

    html_content = response.read().strip()
    import json
    obj_array = json.loads(html_content)
    return obj_array


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#print get_request('http://api.wandoujia.com/v1/apps/com.zhan_dui.animetaste?id=zuimeiyingyong&timestamp=139390842495&token=1c20770a94fb2bd99f10b97228e9a381')
#print get_request('http://itunes.apple.com/lookup?id=739652274')