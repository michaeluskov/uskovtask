var cookieStringToDict = function(cookieString) {
    var dict = {};
    var re = / ?([^;]*?)\=([^;]*?)(;|$)/g;
    var sub;
    while (sub = re.exec(cookieString)) {
        dict[sub[1]] = sub[2];
    };
    return dict;
};


var getCookie = function(key) {
    return cookieStringToDict(document.cookie)[key];
};

var deleteCookie = function(key) {
    document.cookie = key + '=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC';
};

var setCookie = function(key, value) {
    document.cookie = key + '=' + value + '; path=/';
};