// Get the section element container
var sectionContainer = document.getElementById("dates-link-section");
// Get all links with id="date-link" inside the section element container
var links = sectionContainer.getElementsByClassName("date-link");
// Loop through the links and add the active class to the current/clicked link
for (var i = 0; i < links.length; i++) {
  links[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("date-link active");
      console.log(current);
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
    
  });
}