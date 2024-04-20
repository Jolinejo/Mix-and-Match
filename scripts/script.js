const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imgView = document.getElementById("img-view");

inputFile.addEventListener("change", uploadImage);

$("#skincolor").change(function(){
  var hexCode = $(this).val();
 
  // Remove the old paragraph if it exists
  $('#colorchoice p').remove();
 
  // Create a new paragraph element
  var p = document.createElement('p');
  // Set the text content of the paragraph to display the chosen skin color
  
  fetch(`http://127.0.0.1:5001/ask?hex_code=${encodeURIComponent(hexCode)}`, {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
              p.textContent = data.text;
            })
            .catch(error => console.error('Error:', error));
 
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



