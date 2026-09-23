<?php
$username = $_POST['username'];
$password = $_POST['password'];

// Connect to database
$conn = new mysqli("localhost", "root", "", "app_db");

// Insecure query construction
$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = $conn->query($query);

if ($result->num_rows > 0) {
    echo "Login successful! Welcome admin.";
} else {
    echo "Invalid credentials.";
}
?>