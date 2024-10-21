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

function checkPasswordStrength() {
  const password = document.getElementById('password').value;
  const strength = document.getElementById('password-strength');
}
// Regular expressions for password validation
const lowercase = /[a-z]/;
const uppercase = /[A-Z]/;
const numbers = /[0-9]/;
const specialChars = /[!@#$%^&*()_+=[\]{};':"\\|,.<>/?]/;

let passwordStrength = 0;
//Check password length
if (password.length >= 8) {
  passwordStrength += 1;
}
//Check for lowercase letters
if (lowercase.test(password)) {
  passwordStrength += 1;
}
//check for numbers
if (numbers.test(password)){
  passwordStrength += 1;
}
//check for uppercase
if (uppercase.test(password)){
  passwordStrength += 1;
}
//Check for special characters
if (specialChars.test(password)){
  passwordStrength += 1;
}
//Display password strength
switch (passwordStrength) {
  case 0;
  case 1;
  case 2;
  strength.innerHTML = 'Password Strength: Weak';
  strength.style.color = 'red';
  break;
  case 3:
  case: 4:
  strength.innerHTML = 'Password Strength: Medium';
  strength.style.color = 'orange';
  break;
  case 5:
  strength.innerHTML = 'Password Strength: Strong';
  strength.style.color = 'green';
  break;
  }
}
