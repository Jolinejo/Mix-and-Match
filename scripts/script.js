const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imgView = document.getElementById("img-view");

inputFile.addEventListener("change", uploadImage);

$("#skincolor").change(function(){
  var chosenColor = $(this).val();
 
  // Remove the old paragraph if it exists
  $('#colorchoice p').remove();
 
  // Create a new paragraph element
  var p = document.createElement('p');
  // Set the text content of the paragraph to display the chosen skin color
  p.textContent = 'Your skin tone is ' + chosenColor;
 
  // Append the paragraph to the div with ID 'colorchoice'
  $('#colorchoice').append(p);
 });

function uploadImage() {
  let imgLink = URL.createObjectURL(inputFile.files[0]);
  imgView.innerHTML = ''; // Clear any previous content
  imgView.style.backgroundImage = `url(${imgLink})`;
  imgView.style.backgroundSize = 'contain'; // or 'cover'
  imgView.style.backgroundRepeat = 'no-repeat';
  imgView.style.backgroundPosition = 'center center';
  
}



