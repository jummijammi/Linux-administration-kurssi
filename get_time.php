<?php
$host = 'localhost';
$db = 'oma_tietokanta';
$user = 'exampleuser';
$pass = 'change_this_strong_password';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die("Yhteys epäonnistui: " . $conn->connect_error);
}

$sql = "SELECT current_time FROM server_time ORDER BY id DESC LIMIT 1";
$result = $conn->query($sql);

if ($row = $result->fetch_assoc()) {
    echo json_encode(['time' => $row['current_time']]);
} else {
    echo json_encode(['time' => null]);
}

$conn->close();
?>