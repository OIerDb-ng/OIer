<?php
require_once 'common.php';
error_reporting(0);
header("Access-Control-Allow-Origin: http://www.bytew.net, http://xn--vuqs4zq3d.com");
header("Content-type: text/html; charset=utf8");

if ($_SERVER["REQUEST_METHOD"] != "GET")
    die(json_encode(array('result' => array(), 'count' => 0, 'cities' => array())));
$conn = get_database_connection();
$result = array();
$stmt = $conn->prepare("SELECT * FROM `OI_school` WHERE `id` = ?");
$id = (int)$_GET['id'];
$stmt->bind_param('i', $id);
$stmt->execute();
$res = $stmt->get_result();
$result['result'] = $res->fetch_all(MYSQLI_ASSOC);
$result['count'] = $res->num_rows;
echo json_encode($result);
$conn->close();
