# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import csv
import datetime
import pymongo

mongoconn = pymongo.Connection('182.92.163.118', 27017)
cars_db = mongoconn['yaoqingka']["cards"]
# # created_at需要创建索引  db.cards.ensureIndex({x:1})  查看索引 db.test.getIndexes()删除索引：db.test.dropIndex({"username":1})

with open('邀请卡统计.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')
    spamwriter.writerow(['创建时间', '模板id', '发送人', '接收人', '标题', '会议时间', '会议地点', '会议内容'])
    for item in cars_db.find({
        "created_at": {'$gte': datetime.datetime(2014, 7, 1, 0, 0),
                       '$lte': datetime.datetime(2014, 8, 1, 0, 0)}}).sort(
            "created_at", pymongo.ASCENDING):
        print item
        print item['_id']
        print item['recipient']
        print item['content']
        print item['addressor']
        print item['card_image']
        # print item['image_top']
        print item['card_image2']
        print item['share_image']
        print item['word_postion']
        print item['meeting_time']
        print item['meeting_location']
        print item['word_color']
        print item['bg_color']
        # print item['title_color']
        print item['template_card_id']
        print item['title']
        print item['created_at']

        spamwriter.writerow([item['created_at'].strftime('%Y-%m-%d %H:%M:%S'), item['template_card_id'],
                             item['addressor'],
                             item['recipient'], item['title'],
                             item['meeting_time'],
                             item['meeting_location'],
                             item['content']])

