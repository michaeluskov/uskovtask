var isLoading = 0;

var ajaxGet = function(link, cb) {
    var xmlhttp = getXmlHttp()
    xmlhttp.open('GET', link, true);
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4) {
         if(xmlhttp.status == 200) {
           cb(xmlhttp.responseText);
        }
      }
    };
    xmlhttp.send(null);
} ;

var vote = function(poll, variant) {
    if (isLoading)
        return;
    isLoading = 1;
    showLoading(poll);
};

var unvote = function(poll) {
    if (isLoading)
        return;
    isLoading = 1;
    showLoading(poll);
};

var showLoading = function(poll) {
    document.getElementById('polls-loading-'+poll).style.display = 'block';
}

var hideLoading = function(poll) {
    document.getElementById('polls-loading-'+poll).style.display = 'none';
}

var setOnclicks = function() {
    var elements = document.getElementsByTagName('DIV');
    for (var i=0; i<elements.length; i++) {
        var sets = elements[i].id.split('-');
        if (sets.length != 1 || sets[0] == 'polls') {
            if (sets[1] == 'vote') 
                elements[i].onclick = (function(p,v) {return function(){ vote(p,v) }})(sets[2], sets[3]);
            if (sets[2] == 'unvote')
                elements[i].onclick = (function(p) {return function(){ unvote(p) }})(sets[2]);  
        }
    }
};

var init = function() {
    setOnclicks();    
};

window.onload = init;