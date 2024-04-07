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
function addToCart() {
    var quantity = document.getElementById('quantity').value;
    var id = document.getElementById('id').value;

    var itemData = {
        id: id,
        quantity: quantity,
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/cart", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
          console.log(xhr.response);
        } else {
          console.log(`Error: ${xhr.status}`);
        }
    };
    xhr.send(JSON.stringify(itemData));
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
                document.getElementById('id').value = itemId;
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

// Account CRUD
// Create

// Delete
function confirmDelete() {
    if (confirm("Are you sure you want to delete your account?")) {
        deleteAccount();
    }
}
function deleteAccount() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/delete-account", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert("Your account has been deleted.");
            window.location.href = "/home";
        }
    };
    xhr.send();
}
