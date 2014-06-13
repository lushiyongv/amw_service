// GA 统计的变量
var source = "direct",
    url_search_value = window.location.search,
    structured_url_path = location.protocol + '//' + location.host + location.pathname,
    device,
    platform,
    event_info;

// 判断source
if (url_search_value.length > 0) {
    source = url_search_value;
}

// 判断是否是手机
function mobilecheck() {
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return true;
    }
}

if (mobilecheck()) {
    device = "Mobile"
} else {
    device = "Web"
}

// 检测设备系统

function detect_mobile_platform() {

    if (navigator.userAgent.match(/iPhone/i)) {
        return 'iPhone';
    } else if (navigator.userAgent.match(/iPod/i)) {
        return 'iPod';
    } else if (navigator.userAgent.match(/iPad/i)) {
        return 'iPad';
    } else if (navigator.userAgent.match(/Android/i)) {
        return 'Android';
    } else if (navigator.userAgent.match(/webOS/i)) {
        return 'webOS';
    } else if (navigator.userAgent.match(/Windows Phone/i)) {
        return 'WindowsPhone';
    } else {
        return 'Others'
    }

}
platform = detect_mobile_platform();

function event_tracker(name, source, id) {
    event_info = name + '-' + device + '-' + platform;
    ga('send', 'event', event_info, source, card_id);
}