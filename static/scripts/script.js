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
  
  // Assuming hexCode is defined somewhere in your code
fetch(`http://127.0.0.1:5001/ask?hex_code=${encodeURIComponent(hexCode)}`, {
  method: 'GET',
})
.then(response => response.json())
.then(data => {
 const colorChoiceDiv = document.getElementById('output');
 colorChoiceDiv.innerHTML = '';
 // Create and append the season name
 const seasonName = document.createElement('h2');
 seasonName.textContent = data.season;
 colorChoiceDiv.appendChild(seasonName);

 const result = {
  season: data.season,
  matchingColors: {},
  bestHairColors: {}
};

 // Create a div to hold the matching colors
 const matchingColorsHeader = document.createElement('h3');
 matchingColorsHeader.textContent = 'Matching Colors';
 colorChoiceDiv.appendChild(matchingColorsHeader);

 const matchingColorsDiv = document.createElement('div');
 matchingColorsDiv.classList.add('matching-colors-container'); // Add a class for styling
 colorChoiceDiv.appendChild(matchingColorsDiv);

 // Iterate over the matching colors
 for (let i = 0; i < data['matching colors'].length; i += 2) {
    // Create a div for each color pair
    const colorPairDiv = document.createElement('div');
    colorPairDiv.classList.add('color-pair'); // Add a class for styling

    // Create a paragraph for the color name
    const colorName = document.createElement('p');
    colorName.textContent = data['matching colors'][i][0];
    colorPairDiv.appendChild(colorName);

    // Create a paragraph for the color hex code as background color
    const colorHex = document.createElement('p');
    colorHex.textContent = data['matching colors'][i + 1][0];
    let code = data['matching colors'][i + 1][0];
    if (!code.startsWith("#")) {
      code = "#" + code;
    }
    colorHex.style.backgroundColor = `${code}`;
    colorPairDiv.appendChild(colorHex);

    // Append the color pair div to the matching colors container
    matchingColorsDiv.appendChild(colorPairDiv);
    result.matchingColors[data['matching colors'][i][0]] = code;
 }

 const bestHairColorsHeader = document.createElement('h3');
 bestHairColorsHeader.textContent = 'Best Hair Colors';
 colorChoiceDiv.appendChild(bestHairColorsHeader);

  // Create a div to hold the best hair colors
  const bestHairColorsDiv = document.createElement('div');
  bestHairColorsDiv.classList.add('best-hair-colors-container'); // Add a class for styling
  colorChoiceDiv.appendChild(bestHairColorsDiv);
 
  // Split the best hair color string into an array of color names and hex codes
  const bestHairColors = data['best hair color'].split(', ');
 
  // Iterate over the best hair colors
  for (let i = 0; i < bestHairColors.length; i += 2) {
     // Create a div for each hair color pair
     const hairColorPairDiv = document.createElement('div');
     hairColorPairDiv.classList.add('color-pair'); // Add a class for styling
 
     // Create a paragraph for the hair color name
     const hairColorName = document.createElement('p');
     hairColorName.textContent = bestHairColors[i];
     hairColorPairDiv.appendChild(hairColorName);
 
     // Create a paragraph for the hair color hex code as background color
     const hairColorHex = document.createElement('p');
     hairColorHex.textContent = bestHairColors[i + 1];
     let code = bestHairColors[i + 1];
     if (!code.startsWith("#")) {
      code = "#" + code;
    }
     hairColorHex.style.backgroundColor = `${code}`;
     hairColorPairDiv.appendChild(hairColorHex);
 
     // Append the hair color pair div to the best hair colors container
     bestHairColorsDiv.appendChild(hairColorPairDiv);
     result.bestHairColors[bestHairColors[i]] = code;
  }

  fetch('/user/update', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(result)
  })
  .then(response => {
    if (response.ok) {
      console.log('User updated successfully');
    } else {
      console.error('Failed to update user');
    }
  })
  .catch(error => {
    console.error('Error updating user:', error);
  });

})
.catch(error => console.error('Error:', error));

 
  // Append the paragraph to the div with ID 'colorchoice'

  //$('#colorchoice').append(p);
 });

function uploadImage() {
  let imgLink = URL.createObjectURL(inputFile.files[0]);
  imgView.innerHTML = ''; // Clear any previous content
  imgView.style.backgroundImage = `url(${imgLink})`;
  imgView.style.backgroundSize = 'contain'; // or 'cover'
  imgView.style.backgroundRepeat = 'no-repeat';
  imgView.style.backgroundPosition = 'center center';
  
}


document.addEventListener('DOMContentLoaded', function() {
  // Event listener for sign-out button
  document.getElementById('signOutBtn').addEventListener('click', function() {
      // Assuming you have a sign-out endpoint '/signout'
      fetch('http://127.0.0.1:5001/user/signout', {
          method: 'GET',
      })
      .then(response => {
          if (response.ok) {
              // Sign out successful, redirect to login page or perform any other action
              window.location.href = '/homepage/'; // Redirect to login page
          } else {
              // Handle sign out failure
              console.error('Sign out failed:', response.statusText);
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  });
});

document.getElementById('dashboardBtn').addEventListener('click', function() {
  window.location.href = '/dashboard';
});
