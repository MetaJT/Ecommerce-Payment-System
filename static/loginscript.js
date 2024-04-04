// Function to handle button clicks
function signInUser(userId) {
    // Make an AJAX request to Flask backend
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/user-login?userID=' + userId, true);
    xhr.onload = function() {
        if (xhr.status == 200) {
            console.log(xhr.responseText);
            var response = JSON.parse(xhr.responseText);
            if (response) {
                console.log(response.user.FirstName);
                document.getElementById('email').value = response.user.Email;
                document.getElementById('password').value = response.user.Password;
            } else {
                // Handle error or no username found
                console.error('No username found');
            }
        }
    };
    xhr.send();
}
document.addEventListener('DOMContentLoaded', function() {
    var userButtons = document.querySelectorAll('.user-button');
    userButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            signInUser(button.id);
        })
    })
});
