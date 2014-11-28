

var sendResolution = function() {
   var width = window.screen.width;
   var height = window.screen.height;
   var r = new XMLHttpRequest();
   r.open('GET', '/views/addresolution?width='+width+'&height='+height, true);
   r.send();
};




if (window.addEventListener) {
    window.addEventListener('load', function() {
       sendResolution();
    });
} else {
    window.attachEvent('onload', function() {
       sendResolution();
    });
}

