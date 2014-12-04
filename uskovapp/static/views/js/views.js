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

var ajaxGetAndHandle = function (url, cb) {
  var xmlhttp = getXmlHttp()
  xmlhttp.open('GET', url, true);
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
       if(xmlhttp.status == 200) {
         cb(xmlhttp.responseText);
           }
    }
  };
  xmlhttp.send(null);
};

var changeSession = function(id) {
   document.getElementById('views-loading').style.display = 'inline';
   ajaxGetAndHandle('/views/ajax_visits?id='+id, function(resp) {
        document.getElementById('requests-div').innerHTML = resp;
        document.getElementById('views-loading').style.display = 'none';
   });
};

var initViews = function() {
   pSet = document.getElementsByTagName('p');
   for (var p=0; p<pSet.length; p++) {
      pSet[p].onclick = (function(id) {return function() {changeSession(id)} })(pSet[p].id);   
   }
};

if (window.addEventListener) {
    window.addEventListener('load', function() {
       initViews();
    });
} else {
    window.attachEvent('onload', function() {
       initViews();
    });
}