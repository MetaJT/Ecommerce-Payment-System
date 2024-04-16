// Account Management
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
function confirmDelete(event) {
    event.preventDefault(); // Prevent the default form submission behavior
    if (confirm("Are you sure you want to delete your account?")) {
        deleteAccount();
    }
}
function deleteAccount() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/delete-account", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                alert("Your account has been deleted.");
                window.location.href = "/home";
            } else {
                alert("Failed to delete your account.");
            }
        }
    };
    xhr.send();
}

function updateAccount(event) {

    event.preventDefault(); // Prevent the default form submission behavior

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const username = document.getElementById('username').value;

    const accountInfo = {
        email: email,
        password: password,
        username: username
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/edit-account-details", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        console.log(xhr.status)
        if (xhr.readyState == 4) {
            console.log(xhr)
            if (xhr.status == 200) {
                console.log(xhr)
                alert("User information updated successfully!");
            } else {
                alert("Failed to update user information.");
            }
            window.location.href = "/account/settings";
        }
    };
    console.log(accountInfo);
    xhr.send(JSON.stringify(accountInfo));
}

// Cart Management
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
            alert("Item added to cart.")
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
                console.log(response.item);
                document.getElementById('name').innerText = response.item.Name;
                document.getElementById('quantity').innerText = response.item.Quantity;
                document.getElementById('price').innerText = response.item.Price;
                document.getElementById('id').value = itemId;
                document.getElementById('size').innerText = response.item.Size;
            } else {
                console.error('No item found');
            }
        }
    };
    xhr.send();
}
function updateQuantity(cartID) {
    var newQuantity = document.getElementById("quantity_" + cartID).value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/update-quantity", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            window.location.reload();
            alert("Quantity updated.");
        }
    };
    xhr.send(JSON.stringify({cartID: cartID, newQuantity: newQuantity}));
}
function removeItem(cartID) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/remove-item", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert("Item removed from cart.");
            window.location.reload();
            console.log(xhr.response);
        } else {
        console.log(`Error: ${xhr.status}`);
        }
    };
    xhr.send(JSON.stringify({cartID: cartID}));
}
function checkout() {
    // Still need
    alert("Proceeding to checkout.");
}

function submit_purchase() {
    fetch('/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            alert("Purchase Complete!");
            window.location.href = '/home';
        } else {
            console.error("Failed to complete purchase:", response.statusText);
            alert("Failed to complete purchase. Please try again later.");
        }
    })
    .catch(error => {
        console.error("Error submitting purchase:", error);
        // Show an error message to the user
        alert("An error occurred while submitting the purchase. Please try again later.");
    });
}


// Button 
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
// Toggle button
function toggleForm(formId) {
    var form = document.getElementById(formId);
    form.classList.toggle('hidden');
}
