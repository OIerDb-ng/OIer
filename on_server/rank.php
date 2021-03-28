<?php
require_once 'common.php';

error_reporting(0);
header("Access-Control-Allow-Origin: http://www.bytew.net, http://xn--vuqs4zq3d.com");
header("Content-type: text/html; charset=utf8");

if ($_SERVER["REQUEST_METHOD"] != "GET")
    die(json_encode(array('result' => array(), 'count' => 0, 'cities' => array())));

$conn = get_database_connection();
$result = array();

$options = array('province', 'city');

$page = (int)$_GET["page"];
$page = $page > 0 ? $page : 1;
$page = $page * 10 - 10;

$conditions = array();
$params = array('');
foreach ($options as $key) {
    if (empty($_GET[$key])) continue;
    array_push($conditions, "$key=?");
    $params[0] .= 's';
    array_push($params, $_GET[$key]);
}
$where_query = empty($conditions) ? "" : " WHERE " . join(' AND ', $conditions);
$query =
    "SELECT `id`,`name`,`rating`,`division`,`province`,`city`,`rank` FROM `OI_school` " .
    $where_query . " " .
    "ORDER BY `rating` DESC LIMIT $page,10";
$res = query_assoc_all($conn, $query, $params[0], array_slice($params, 1));
$result['result'] = $res;
$result['count'] = count($res);
$result['cities'] = array();

if (!empty($_GET["province"])) {
    $query =
        "SELECT `city` FROM `OI_school` " .
        "WHERE `province` = ? " .
        "GROUP BY city ORDER BY SUM(`rating`) DESC";
    foreach (query_assoc_all($conn, $query, 's', array($_GET["province"])) as $row)
        array_push($result['cities'], $row["city"]);
}

echo json_encode($result);
$conn->close();
