var isLoading = 0;

var getXmlHttp = function() {
  var xmlhttp;
  try {
    xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e) {
    try {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (E) {
      xmlhttp = false;
    }
  }
  if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
  }
  return xmlhttp;
};

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
    ajaxGet('/polls/vote?poll='+poll+'&variant='+variant, function(res) {
        document.getElementById('polls-wrapper-'+poll).innerHTML = res;
        setOnclicks();
        isLoading = 0;
    });
};

var unvote = function(poll) {
    if (isLoading)
        return;
    isLoading = 1;
    showLoading(poll);
    ajaxGet('/polls/unvote?poll='+poll, function(res) {
        document.getElementById('polls-wrapper-'+poll).innerHTML = res;
        setOnclicks();
        isLoading = 0;
    });
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
        if (sets.length != 1 && sets[0] == 'polls') {
            if (sets[1] == 'vote') 
                elements[i].onclick = (function(p,v) {return function(){ vote(p,v) }})(sets[2], sets[3]);
            if (sets[1] == 'unvote')
                elements[i].onclick = (function(p) {return function(){ unvote(p) }})(sets[2]);  
        }
    }
};

var updateResultPics = function() {
    var els = document.getElementsByTagName('IMG');
    for (var i=0; i<els.length; i++) {
        var sets = els[i].id.split('-');
        if (sets.length != 1 && sets[0] == 'polls' && sets[1] =='image') {
            els[i].src = '/polls/pic/' + sets[2] + '.png#' + new Date().getTime();
        }
    }
};

var init = function() {
    setOnclicks();    
    setInterval(updateResultPics, 3000);
};

window.onload = init;