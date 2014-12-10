var photos = [
                ['armin', 'http://cs620423.vk.me/v620423922/113e1/Fjb_p_5r2ak.jpg', 'http://cs620423.vk.me/v620423922/113e0/VD0Cd6xU0mo.jpg'],
                ['voronin', 'http://cs625429.vk.me/v625429642/41e/zTb3H17p6mM.jpg', 'http://cs625429.vk.me/v625429642/41d/xEmfH3uSS3g.jpg'],
                ['risovach', 'http://risovach.ru/upload/2013/06/generator/udivlenie_22496303_orig_.jpeg', 'http://risovach.ru/upload/2013/06/generator/udivlenie_22496303_orig_.jpeg'],
                ['obama', 'http://www.lie-emotions.com.ua/stati/POL/3/udivlenie_ehmocija.jpg', 'http://www.lie-emotions.com.ua/stati/POL/3/udivlenie_ehmocija.jpg'],
                ['kirkorov', 'http://risovach.ru/upload/2012/05/templ_1338476285_orig_Udivlenie.jpg', 'http://risovach.ru/upload/2012/05/templ_1338476285_orig_Udivlenie.jpg']
             ];
             
var thumbs = [];

var imgNodes = {};

var isLoaded = {};

var bubbleId = 0;

var photoViewMode = false;

var currentPhoto = photos.length + 1;

var disableViewMode = function() {
    photoViewMode = false;
    document.getElementById('photo-view').style.display = 'none';
    document.getElementById('photo-help').style.display = 'none';
    document.location.hash = '';
}

var enableViewMode = function() {
    photoViewMode = true;
    document.getElementById('photo-view').style.display = 'block';
    document.getElementById('photo-view').onclick = function(e) {
        e = e || window.event;
        disableViewMode();
    };
    document.getElementById('photo-view-border').onclick = function(e) {
        e = e || window.event;
        preventDefault(e);
        stopPropagation(e);
        return false;
    };
    document.getElementById('photo-view-close-cross').onclick = function(e) {
        e = e || window.event;
        disableViewMode();
    };
    document.getElementById('photo-view-right-button').onclick = function(e) {
        e = e || window.event;
        showPhoto(currentPhoto+1);
    };
    document.getElementById('photo-view-left-button').onclick = function(e) {
        e = e || window.event;
        showPhoto(currentPhoto-1);
    };  
    document.onkeydown = function(e) {
        e = e || window.event;
        switch(e.which || e.keyCode) {
            case 37:
                if (photoViewMode) {
                    preventDefault(e);
                    showPhoto(currentPhoto-1);
                }
                break;
            case 39:
                if (photoViewMode) {
                    preventDefault(e);
                    showPhoto(currentPhoto+1);
                }
                break;
            case 27:
                preventDefault(e);
                disableViewMode();
                break;
            case 112:
                preventDefault(e);
                stopPropagation(e);
                toggleHelp();
                break;
            case 116:
                if (photoViewMode) {
                    preventDefault(e);
                    saveStartPhoto();
                }
                break;
            case 115:
                preventDefault(e);
                deleteStartPhoto();
                break;
            case 117:
                if (photoViewMode) {
                    preventDefault(e);
                    saveBgPhoto();
                }
                break;
            case 118:
                preventDefault(e);
                deleteBgPhoto();
                break;
        }
    };
    ie8DirtyHacks();
};

var toggleHelp = function() {
    if (!photoViewMode)
        return;
    var help = document.getElementById('photo-help');
    help.style.display = (help.style.display == 'none') ? 'block' : 'none';
};

var getImgNode = function(i) {
    i = parseInt(i);
    if (i<0 || i>=photos.length) return;
    var node = document.createElement('IMG');
    node.id = 'photo-view-img';
    node.className = 'photo-view-img';
    node.alt = 'Photo';
    addEvent(node, 'load', function() {
        isLoaded[i] = true;
        if (currentPhoto == i) 
            document.getElementById('photo-view-loading').style.display = 'none';
    });
    node.src = photos[i][2];
    return node;
};

var showPhoto = function(i) {
    if (i<0 || i>=photos.length)
        return;
    if (currentPhoto != photos.length + 1)
        document.getElementById('photo-view-img').parentNode.removeChild(document.getElementById('photo-view-img'));
    var child = document.getElementById('photo-view-space');
    document.getElementById('photo-view-space').style.display = 'block';
    currentPhoto = i;
    if (imgNodes[currentPhoto] === undefined) {
        imgNodes[currentPhoto] = getImgNode(currentPhoto);
    }
    document.location.hash = '#' + photos[currentPhoto][0];
    if (currentPhoto == 0)
        document.getElementById('photo-view-left-button').style.display = 'none';
    else    
        document.getElementById('photo-view-left-button').style.display = 'block';
    if (currentPhoto == photos.length-1)
        document.getElementById('photo-view-right-button').style.display = 'none';
    else    
        document.getElementById('photo-view-right-button').style.display = 'block';
    if (!isLoaded[currentPhoto])
        document.getElementById('photo-view-loading').style.display = 'block';
    document.getElementById('photo-view-space').appendChild(imgNodes[currentPhoto]);
    if (i>0 && !imgNodes[i-1])
        imgNodes[i-1] = getImgNode(i-1);
    if (i!=photos.length-1 && !imgNodes[i+1])
        imgNodes[i+1] = getImgNode(i+1);
};

var saveStartPhoto = function() {
    setCookie('start-photo', currentPhoto);
    showMessageBubble('Стартовое фото сохранено');
};

var deleteStartPhoto = function() {
    deleteCookie('start-photo');
    showMessageBubble('Стартовое фото удалено');
};

var saveBgPhoto = function() {
    setCookie('background', photos[currentPhoto][2]);
    document.body.style.background = 'url(' + photos[currentPhoto][2] + ')';
    showMessageBubble('Фон сохранен');
};

var deleteBgPhoto = function() {
    deleteCookie('background');
    document.body.style.background = '#FFFFFF';
    showMessageBubble('Фон удален');
};

var photoThumbClick = function(i) {
    enableViewMode();
    showPhoto(i);
};

var getPhotoThumbElement = function(i) {
    if (i<0 || i>=photos.length) return;
    var photoThumb = document.createElement('DIV');
    photoThumb.className = "photo-thumb-wrapper";
    var img = document.createElement('IMG');
    img.className = "photo-thumb";
    img.src = photos[i][1];
    photoThumb.appendChild(img);
    return photoThumb;
};

var getClearer = function(isFinal) {
    var clearer = document.createElement('DIV');
    clearer.className = isFinal ? 'final-clearer' : 'clearer';
    return clearer;
};
             
             
var fillThumbSpace = function() {
    var thumbSpace = document.getElementById('photo-thumb-space');
    for (var i=0; i<photos.length; i++) {
        var photoThumb = getPhotoThumbElement(i);
        photoThumb.onclick = (function() {var n=i; return function(){photoThumbClick(n)}})();
        thumbSpace.appendChild(photoThumb);
        thumbs.push(photoThumb);
        if ((i+1)%3 == 0) {
            thumbSpace.appendChild(getClearer());        
        }
    }
    thumbSpace.appendChild(getClearer(1)); 
};        


var showMessageBubble = function(text) {
    clearInterval(bubbleId);
    document.getElementById('photo-bubble').innerHTML = text;
    document.getElementById('photo-bubble').style.display = 'block';
    bubbleId = setTimeout(function() {
        document.getElementById('photo-bubble').style.display = 'none';
    }, 2000);
};

var showPhotoFromHash = function() {
    var id = document.location.hash.substring(1);
    for (var i=0; i<photos.length; i++) {
        if (photos[i][0] == id)
            break;
    }
    if (i < photos.length) {
        enableViewMode();
        showPhoto(i);
    } else {
        disableViewMode();    
    }
};

var handleHashChange = function() {
    var lastHash = document.location.hash;
    setInterval(function() {
        if (document.location.hash != lastHash) {
            lastHash = document.location.hash;
            showPhotoFromHash();
        }
    }, 100);
};

var init = function() { 
    fillThumbSpace();
    document.getElementById('photo-thumb-clear-start-photo').onclick = deleteStartPhoto;
    document.getElementById('photo-thumb-clear-background').onclick = deleteBgPhoto;
    if (document.location.hash != '' && document.location.hash != '#') {
        showPhotoFromHash();
    } else if (getCookie('start-photo')) {
        enableViewMode();
        showPhoto(getCookie('start-photo'));
    }
    handleHashChange();
}; 

var preventDefault = function(e) {
    if (!e) return;
    if ('preventDefault' in e) 
        e.preventDefault();
    else {
        e.keyCode = 0;
        window.event.keyCode = 0;
        e.returnValue = false;
        window.event.returnValue = false;
    }
};

var stopPropagation = function(e) {
    if (!e) return;
    if ('stopPropagation' in e)  e.stopPropagation();
    else e.cancelBubble = true;
};

var addEvent = function(object, event, handler) {
    if (object.addEventListener) {
        object.addEventListener(event, handler);
    } else {
        object.attachEvent('on' + event, handler);    
    }
};

addEvent(window, 'load', init);

var ie8DirtyHacks = function() {
     window.onhelp = function() {
            if (photoViewMode)
                return false;
        };
    if ('attachEvent' in window) {
        window.onhelp = function() {
            if (photoViewMode)
                return false;
        };
        window.attachEvent('onbeforeunload', function() {
            if (photoViewMode) 
                return false;
        });
    }
}