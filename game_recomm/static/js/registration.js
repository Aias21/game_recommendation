document.getElementById("registration-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const data = {
        username: username,
        email: email,
        password: password
    };

    fetch("register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById("response").textContent = "Registration successful!";
    })
    .catch(error => {
        document.getElementById("response").textContent = "Registration failed.";
    });
});