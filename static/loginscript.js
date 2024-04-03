// Function to handle button clicks
function signInUser(userId) {
    // Make an AJAX request to Flask backend
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/login-user?userID=' + userId, true);
    xhr.onload = function() {
        if (xhr.status == 200) {
            console.log(xhr.responseText);
            var response = JSON.parse(xhr.responseText);
            if (response) {
                console.log(response.user.FirstName);
                document.getElementById('user').innerText = response.user.FirstName;
            } else {
                // Handle error or no username found
                console.error('No username found');
            }
        }
    };
    xhr.send();
}
document.addEventListener('DOMContentLoaded', function() {
    // Your JavaScript code here
    var alexButton = document.getElementById('Alex');
    var jordanButton = document.getElementById('Jordan');
    var barackButton = document.getElementById('Barack');

    // Add event listeners to buttons
    jordanButton.addEventListener('click', function() {
        signInUser('1');
    });

    alexButton.addEventListener('click', function() {
        signInUser('2');
    });

    barackButton.addEventListener('click', function() {
        signInUser('3');
    });
});
