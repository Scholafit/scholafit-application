const isMobile = /Android|webOS|iphone|ipad|ipod|BlackBerry|IEMobile|OPera Mini/i.test(navigator.userAgent);
let d = new Date();
Document.body.innerHTML = "<h1>Today's date is" + d + "</h1>"
document.addEventListener("DOMContentLoaded", function()  {
  var elements = document.querySelectorAll(".fade-in");
  elements.forEach(function(element) {
    element.style.opacity = 0;
    element.style.filter= "alpha(opacity=0)";
    var opacity = 0;
    setnterval(function(){
      opacity += 0.1;
      element.style.opacity = opacity;
      element.style.filter = "alpha(opacity=" + opacity * 100 + ")";
      if (opacity >= 1){
        clearInterval(interval);
      }
    }, 50);
  });
});
