document.addEventListener('DOMContentLoaded', function () {
    // Log In Form
    document.getElementById('logInForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission
        let formData = new FormData(this);
        let jsonData = {};
        for (const [key, value] of formData.entries()) {
            jsonData[key] = value;
        }
        const jsonBody = JSON.stringify(jsonData);

        // Send JSON data in fetch request
        fetch('http://127.0.0.1:5001/user/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify content type as JSON
            },
            body: jsonBody
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/upload/';
            } else {
                return response.json();
            }
        }).then(data => {
            if (data && data.error) {
                // Display error message in the error paragraph
                const errorParagraph = document.querySelector('.error');
                errorParagraph.textContent = data.error;
                errorParagraph.classList.remove('error--hidden');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
