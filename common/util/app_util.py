#coding=utf-8
import time
import hashlib
import json

from django.conf import settings

from articles.models import Writer, Platform
from nice_http_util import get_request


def parse_download_url(url):
    """解析APP下载链接"""
    # http://itunes.apple.com/lookup?id=739652274
    # https://itunes.apple.com/cn/app/zui-mei-ying-yong/id739652274?mt=8
    writer = Writer()
    writer.download_url = url
    if url.find('itunes.apple.com') != -1:
        # IOS APP
        id = url[(url.index('id') + len('id')):url.index('?')]
        ios_url = 'http://itunes.apple.com/lookup?id=%s' % id
        ios_json = get_request(ios_url)['results'][0]
        return parse_ios_json(ios_json, writer)

    # http://www.wandoujia.com/apps/com.zhan_dui.animetaste
    elif url.find('www.wandoujia.com') != -1:
        # Android APP
        id = settings.WANDOUJIA_ID
        key = settings.WANDOUJIA_AUTHKEY
        timestamp = str(int(time.time()*100))
        token = hashlib.md5(id+key+timestamp).hexdigest()
        package_name = url[(url.rindex('/')+1):]
        android_url = 'http://api.wandoujia.com/v1/apps/%s?id=%s&timestamp=%s&token=%s' \
                      % (package_name, id, timestamp, token)
        wandouja_json = get_request(android_url)
        return parse_wandoujia_json(wandouja_json, writer)

    return None


def parse_wandoujia_json(wandoujia_json, writer):
    """
    {"apks":[{"adsType":"NONE","bytes":6540430,"creation":1390583414000,
    "downloadUrl":{"market":"官方",
    "url":"http://apps.wandoujia.com/redirect?signature=d889470&url=http%3A%2F%2Fapk.wdjcdn.com%2Fd%2F33%2F1fb104fca87629c62e174d6f108db33d.apk&pn=com.zhan_dui.animetaste&md5=1fb104fca87629c62e174d6f108db33d&apkid=9163239&vc=15&size=6540430&pos=t/detail&tokenId=zuimeiyingyong&appType=APP"},
    "language":["日语","斯洛维尼亚语","斯瓦西里语","法语","土耳其语","菲律宾语","立陶宛语","斯洛伐克语","芬兰语","捷克语","拉托维亚语","乌克兰语","西班牙语","克罗地亚语","简体中文","泰语","意大利语","保加利亚语","葡萄牙语","爱沙尼亚语","南非荷兰语","俄语","波兰语","希腊语","越南语","匈牙利语","波斯语","韩语","荷兰语","瑞典语","英文","德语","丹麦语","印度语","繁体中文","阿拉伯语","罗马尼亚语"],
    "minSdkVersion":8,"paidType":"NONE","securityStatus":"SAFE",
    "signature":"761f1efdf4f1afe0311c7d36f9099950","superior":1,"verified":3,
    "versionCode":15,"versionName":"1.3.0"}],
    "categories":[{"alias":"entertainment","name":"影音图像","type":"APP"}],
    "changelog":"春节前的一次重大更新！送给广大ATer的新年礼物~ \r<br />【新增】分类功能终于来啦！ \r<br />【新增】可以在App中查看我们的访谈啦！ \r<br />【新增】猜你喜欢有木有？看看AT猜不猜的中你的口味 \r<br />【改进】稳定性增强，速度更优化哦~",
    "description":"AnimeTaste是第一款关注全球独立动画和中国原创动画的App。在这里你可以感受到来自全球各个国家顶尖的动画短片，微电影，电视包装，运动图形等作品，以及来自中国的原创动画力量。品味动画，重拾幻想。 \r<br />AnimeTaste 功能推荐: \r<br />- 精选动画，放飞你的想象力 \r<br />- 在线观看，无需漫长等待 \r<br />- 动画分享，和朋友分享动画的快乐 \r<br />- 动画收藏，随时回味经典 \r<br />品赏艾尼莫(AnimeTaste.net)创建于2008年,是国内唯一关注全球动画短片的网站,坚持为超过14万订阅用户提供国内外最新最精彩的动画欣赏，访谈和专题内容。",
    "developer":{"email":"plidezus@gmail.com","id":7497550,"intro":null,
    "name":"AnimeTaste.net","urls":null,"verified":null,"website":"http://i.animetaste.net",
    "weibo":null},"downloadCount":103647,"downloadCountStr":"10 万",
    "icons":{"px78":"http://img.wdjimg.com/mms/icon/v1/5/ff/bc5d771897e6db6fb092b7daddf1eff5_78_78.png",
    "px48":"http://img.wdjimg.com/mms/icon/v1/5/ff/bc5d771897e6db6fb092b7daddf1eff5_48_48.png"},
    "installedCount":142016,"installedCountStr":"14 万","likesRate":95,
    "packageName":"com.zhan_dui.animetaste","publishDate":1378362092000,
    "screenshots":{"normal":["http://img.wdjimg.com/mms/screenshot/8/fa/721a16296609c7de868055cebb6adfa8_320_533.jpeg",
    "http://img.wdjimg.com/mms/screenshot/f/04/a3fb926af8e32b8915f15dae8ac0704f_320_533.jpeg",
    "http://img.wdjimg.com/mms/screenshot/5/91/4be7d8f4976ad79934306e14f4616915_320_533.jpeg",
    "http://img.wdjimg.com/mms/screenshot/0/3f/7c861d2e10aeb4d5255de9ca7b4ab3f0_320_533.jpeg",
    "http://img.wdjimg.com/mms/screenshot/c/94/f034aa35ab3d9d346cf39b47b19bf94c_320_533.jpeg"],
    "small":["http://img.wdjimg.com/mms/screenshot/8/fa/721a16296609c7de868055cebb6adfa8_200_333.jpeg",
    "http://img.wdjimg.com/mms/screenshot/f/04/a3fb926af8e32b8915f15dae8ac0704f_200_333.jpeg",
    "http://img.wdjimg.com/mms/screenshot/5/91/4be7d8f4976ad79934306e14f4616915_200_333.jpeg",
    "http://img.wdjimg.com/mms/screenshot/0/3f/7c861d2e10aeb4d5255de9ca7b4ab3f0_200_333.jpeg",
    "http://img.wdjimg.com/mms/screenshot/c/94/f034aa35ab3d9d346cf39b47b19bf94c_200_333.jpeg"]},
    "tagline":"品味动画，重拾幻想","tags":[{"tag":"影音图像"}],
    "title":"AnimeTaste"}
    """
    writer.title = wandoujia_json['title']
    writer.sub_title = wandoujia_json['tagline']
    if writer.sub_title is None:
        writer.sub_title = ''
    writer.platform = Platform.objects.get(pk=2)  # android=2,iPhone=1
    writer.digest = wandoujia_json['description']
    writer.icon_image = wandoujia_json['icons']['px48']
    writer.size = wandoujia_json['apks'][0]['bytes']
    return writer


def parse_ios_json(ios_json, writer):
    """
{
 "resultCount":1,
 "results": [
{"kind":"software", "features":[],
"supportedDevices":["iPodTouchThirdGen", "iPadMini4G", "iPodTouchFifthGen", "iPadWifi", "iPadThirdGen", "iPhone5", "iPodTouchourthGen", "iPadMini", "iPad3G", "iPhone4", "iPadThirdGen4G", "iPhone5s", "iPad23G", "iPadFourthGen", "iPad2Wifi", "iPhone5c", "iPadFourthGen4G", "iPhone-3GS", "iPhone4S"], "isGameCenterEnabled":false,
"artistViewUrl":"https://itunes.apple.com/us/artist/li-ma/id739652277?uo=4",
"artworkUrl60":"http://a808.phobos.apple.com/us/r30/Purple/v4/e0/05/43/e00543a1-63f5-8839-c796-d84367fc2bab/icon-57.png",
"screenshotUrls":["http://a3.mzstatic.com/us/r30/Purple/v4/ec/7e/8c/ec7e8c26-83d3-d0c6-0882-b4baa254e4b5/screen1136x1136.jpeg",
"http://a3.mzstatic.com/us/r30/Purple6/v4/4a/f4/ce/4af4ce47-4263-303c-476e-bc7471060217/screen1136x1136.jpeg",
"http://a2.mzstatic.com/us/r30/Purple4/v4/74/ab/ab/74abab21-79d5-df07-204d-614ceb039dba/screen1136x1136.jpeg"],
"ipadScreenshotUrls":[],
"artworkUrl512":"http://a854.phobos.apple.com/us/r30/Purple/v4/8c/b9/c1/8cb9c1b9-6259-410b-6e6d-8c9d4ce59c77/mzl.ptlfezve.png",
"artistId":739652277,
"artistName":"Li Ma", "price":0.00, "version":"1.2.0",
"description":"最美应用致力于发掘功能之美、视觉之美、交互之美、用户体验之美。",
"currency":"USD", "genres":["Utilities"], "genreIds":["6002"],
"releaseDate":"2013-11-24T11:03:24Z", "sellerName":"Li Ma", "bundleId":"com.brixd.niceapps",
"trackId":739652274, "trackName":"最美应用", "primaryGenreName":"Utilities",
"primaryGenreId":6002, "releaseNotes":"增加文章美一下和一般般功能;\n增加评论功能;\n优化体验;修正Bug",
"formattedPrice":"Free", "wrapperType":"software", "contentAdvisoryRating":"4+",
"artworkUrl100":"http://a854.phobos.apple.com/us/r30/Purple/v4/8c/b9/c1/8cb9c1b9-6259-410b-6e6d-8c9d4ce59c77/mzl.ptlfezve.png",
"trackCensoredName":"最美应用", "trackViewUrl":"https://itunes.apple.com/us/app/zui-mei-ying-yong/id739652274?mt=8&uo=4",
"languageCodesISO2A":["EN", "ZH"], "fileSizeBytes":"7247100", "trackContentRating":"4+",
"averageUserRating":5.0, "userRatingCount":5}]
}
    """
    writer.title = ios_json['trackName']
    writer.platform = Platform.objects.get(pk=1)  # android=2,iPhone=1
    writer.digest = ios_json['description']
    writer.icon_image = ios_json['artworkUrl60']
    writer.size = ios_json['fileSizeBytes']
    return writer

if __name__ == '__main__':
    parse_download_url('http://www.wandoujia.com/apps/com.zhan_dui.animetaste')
