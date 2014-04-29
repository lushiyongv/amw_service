amway_service
=============

青英晚会  邀请函

登陆地址：http://a.brixd.com/invitation2014/index.html，   会跳转至：http://amway.brixd.com/qyh

静态资源目录： ~/amway.brixd.com/amway_service/static

前端代码目录： ~/amway.brixd.com/amway_service/templates

日志和统计脚本目录： ~/amway.brixd.com/amway_service/user_login_log  


=============

安利会议  问卷调查  答案日志记录

post上传数据接口：http://amway.brixd.com/conference/survey/answers/

日志目录 ~/amway.brixd.com/amway_service/logs/conference

记录的日志还是按天一天一个文件，除了上传的11个字段， 日志中前两列是ip 和时间2个字段的记录，格式（字段中间tab分割）：
115.183.9.222   2014-04-28 15:44:54     name    srid    identity        telephone       answer1 answer2 answer3 answer4 answer5 answer6 surveylocation
