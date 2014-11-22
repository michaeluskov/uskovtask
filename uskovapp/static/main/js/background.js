var changeBg = function() {
    if (getCookie('background') !== undefined) {
        document.body.style.background = 'url(' + getCookie('background') + ')';    
    }
};


if (window.addEventListener) {
    window.addEventListener('load', function() {
       changeBg();
    });
} else {
    window.attachEvent('onload', function() {
       changeBg();
    });
}