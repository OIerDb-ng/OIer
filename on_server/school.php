<?php
require_once 'common.php';
error_reporting(0);
header("Access-Control-Allow-Origin: http://www.bytew.net, http://xn--vuqs4zq3d.com");
header("Content-type: text/html; charset=utf8");

if ($_SERVER["REQUEST_METHOD"] != "GET")
    die(json_encode(array('result' => array(), 'count' => 0, 'cities' => array())));
$conn = get_database_connection();
$res = query_assoc_all(
    $conn, "SELECT * FROM `OI_school` WHERE `id` = ?",
    'i', array((int)$_GET['id'])
);
$result['result'] = $res;
$result['count'] = count($res);

echo json_encode($result);
$conn->close();
