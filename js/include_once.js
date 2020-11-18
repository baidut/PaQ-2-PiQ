if ($(document).attr('title') == "") { // no head
  if (window._head_loaded === undefined) {
    window._head_loaded = true;
    $(function(){
      document.body.innerHTML = "<div id='header'></div>" + document.body.innerHTML + "<div id='footer'></div>";
      $("#header").load("head.htm");
      $("#footer").load("foot.htm");
    });
      // the rest of your javascript
  }
}

if (window.isMobile == undefined) {
  //global vars
  var isMobile = {
     Android: function() {
         return navigator.userAgent.match(/Android/i);
     },
     BlackBerry: function() {
         return navigator.userAgent.match(/BlackBerry/i);
     },
     iOS: function() {
         return navigator.userAgent.match(/iPhone|iPad|iPod/i);
     },
     Opera: function() {
         return navigator.userAgent.match(/Opera Mini/i);
     },
     Windows: function() {
         return navigator.userAgent.match(/IEMobile/i) || navigator.userAgent.match(/WPDesktop/i);
     },
     any: function() {
         return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
     }
  };
}
