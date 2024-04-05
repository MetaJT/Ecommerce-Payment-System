function signInUser(userId) {
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
                console.error('No username found');
            }
        }
    };
    xhr.send();
}
function selectItem(itemId) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get-item?itemID=' + itemId, true);
    xhr.onload = function() {
        if (xhr.status == 200) {
            console.log(xhr.responseText);
            var response = JSON.parse(xhr.responseText);
            if (response) {
                console.log(response.item.Name);
                document.getElementById('name').innerText = response.item.Name;
                document.getElementById('quantity').innerText = response.item.Quantity;
                document.getElementById('price').innerText = response.item.Price;
            } else {
                console.error('No item found');
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
    var itemButtons = document.querySelectorAll('.item-button');
    itemButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            selectItem(button.id);
        })
    })
});
