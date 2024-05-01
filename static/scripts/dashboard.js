// Fetch user data and populate the webpage
const keys = ['season', 'username', 'matchingColors', 'bestHairColors']; // Specify the keys you want to retrieve
const queryParams = keys.map(key => `keys=${encodeURIComponent(key)}`).join('&');

fetch('/user/data?' + queryParams, {
    method: 'GET',
})
.then(response => {
    if (response.ok) {
        return response.json();
    } else {
        throw new Error('Failed to fetch user data');
    }
})
.then(userData => {
    console.log(userData)

    document.getElementById('userName').textContent = userData.username;
    document.getElementById('userSeason').textContent = userData.season;
    
    const matchingColorsSpan = document.getElementById('userColors');
    for (const colorName in userData.matchingColors) {
        const colorHex = userData.matchingColors[colorName];
        const colorDiv = document.createElement('div');
        colorDiv.textContent = `${colorName}: ${colorHex}`;
        colorDiv.style.backgroundColor = colorHex;
        matchingColorsSpan.appendChild(colorDiv);
    }
    
    const hairColorsSpan = document.getElementById('userHairColors');
    for (const colorName in userData.bestHairColors) {
        const colorHex = userData.bestHairColors[colorName];
        const colorDiv = document.createElement('div');
        colorDiv.textContent = `${colorName}: ${colorHex}`;
        colorDiv.style.backgroundColor = colorHex;
        hairColorsSpan.appendChild(colorDiv);
    }
})
.catch(error => {
    console.error('Error fetching user data:', error);
});
