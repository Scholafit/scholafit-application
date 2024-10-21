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

const postBtn = document.getElementById('post-btn');
postBtn.addEventListener('click', () => {
  e.preventDefault();
  //Sending POST request using Fetch API
  fetch('http://127.0.0.1:5000/api/v1/reset-password/{token}', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
    body: JSON.stringify()
  })
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error(error));
});

//Get elements
const subjectList = document.getElementById('subject-List');
const addSubjectsBtn = document.getElementById('add-subjects-btn');
const selectedSubjectsList = document.getElementById('selected-subjects-List');
//Add event listener to button
addSunjectsBtn.addEventListener('click',() => {
  //Get selected options
  const selectdOptions = Array.from(subjectList.selectedOptions);
  //Clear existing list
  selectedSubjectsList.innerHTML = '';
  //Add selected subjects to list
  selectedOptions.forEach(option) => {
    const ListItem = document.creatElement('Li');
    ListItem.textContent = option.value;

    selectedSubjectsList.appendChild(ListItem);
  });
});
