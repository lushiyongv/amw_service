function shareFriend() {
    if(document.getElementById('sina_share') !== null){
        lineLink = lineLink + '&utm_source=wexin&utm_campaign=referral&utm_medium=weixin';
    }
    WeixinJSBridge.invoke('sendAppMessage', {
        "img_url": imgUrl,
        "img_width": "640",
        "img_height": "640",
        "link": lineLink,
        "desc": descContent,
        "title": shareTitle
    }, function(res) {
        event_tracker('WeixinFriend', source, card_id);
        _report('send_msg', res.err_msg);
    })
}

function shareTimeline() {
    if(document.getElementById('sina_share') !== null){
        lineLink = lineLink + '&utm_source=wexin&utm_campaign=referral&utm_medium=pengyouquan';
    }
    WeixinJSBridge.invoke('shareTimeline', {
        "img_url": imgUrl,
        "img_width": "640",
        "img_height": "640",
        "link": lineLink,
        "desc": descContent,
        "title": shareTitle
    }, function(res) {
        event_tracker('Pengyouquan', source, card_id);
        _report('timeline', res.err_msg);
    });
}

function shareWeibo() {
    if(document.getElementById('sina_share') !== null){
        lineLink = lineLink + '&utm_source=wexin&utm_campaign=referral&utm_medium=tengxunweibo';
    }
    WeixinJSBridge.invoke('shareWeibo', {
        "content": descContent,
        "url": lineLink,
    }, function(res) {
        event_tracker('TengxunWeibo', source, card_id);
        _report('weibo', res.err_msg);
    });
}
// 当微信内置浏览器完成内部初始化后会触发WeixinJSBridgeReady事件。
document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {

    // 发送给好友
    WeixinJSBridge.on('menu:share:appmessage', function(argv) {
        shareFriend();
    });

    // 分享到朋友圈
    WeixinJSBridge.on('menu:share:timeline', function(argv) {
        shareTimeline();
    });

    // 分享到微博
    WeixinJSBridge.on('menu:share:weibo', function(argv) {
        shareWeibo();
    });
}, false);