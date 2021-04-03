<?php
require_once 'common.php';
error_reporting(0);
header("Access-Control-Allow-Origin: http://www.bytew.net, http://xn--vuqs4zq3d.com");
header("Content-type: text/html; charset=utf8");

if ($_SERVER["REQUEST_METHOD"] != "GET") {
    die(json_encode(array('result' => array(), 'count' => 0, 'cities' => array())));
}

function search_specific($limit, $params): array
{
    $conn = get_database_connection();
    $conditions = array();
    $query_params = array();
    $types = '';
    foreach (array('pinyin' => 's', 'name' => 's', 'year' => 'i',) as $item => $key) {
        # exact match
        if (!empty($params[$item])) {
            array_push($conditions, "`$item` = ?");
            array_push($query_params, $params[$item]);
            $types .= $key;
        }
    }
    if (!empty($params['province'])) {
        $province = $params['province'];
        array_push($conditions, "`awards` LIKE ?");
        array_push($query_params, "%$province%");
        $types .= 's';
    }
    if (!empty($params['school'])) {
        $school = $params['school'];
        $school = query_assoc_all($conn,
            "SELECT * FROM OI_school WHERE name LIKE ?",
            's', array("%$school%"));
        if (count($school) > 0) {
            $sid = $school[0]['id'];
            array_push($conditions, "`awards` LIKE ?");
            array_push($query_params, "%'school_id': $sid,%");
        } else {
            array_push($conditions, "`awards` LIKE ?");
            array_push($query_params, "%$school%");
        }
        $types .= 's';
    }
    $res = query_assoc_all(
        $conn,
        "SELECT * FROM `OIers` " .
        "WHERE" . join(" AND ", $conditions) .
        " LIMIT $limit, 20",
        $types, $query_params
    );
    $conn->close();
    return $res;
}

function search_normal($limit, $params): array
{
    $conn = get_database_connection();
    $query_params = array();
    foreach ($params as $keyword) {
        array_push($query_params, $keyword);
        array_push($query_params, $keyword);
        array_push($query_params, $keyword);
        array_push($query_params, "%$keyword%");
    }
    $cur = query_assoc_all(
        $conn,
        "SELECT * FROM `OIers` " .
        "WHERE" . join(" AND ", array_fill(
            0, count($params),
            "(`pinyin` = ? OR `name` = ? OR `re1` = ? OR `awards` like ?)"
        )) .
        " LIMIT $limit, 20",
        str_repeat('ssss', count($params)), $query_params
    ); # SELECT statements are case insensitive
    $conn->close();
    return $cur;
}

$method = $_GET["method"];
$page = (int)$_GET["pages"];
$page = $page > 0 ? $page : 1;
$page = $page * 20 - 20;

$result = array();
switch ($method) {
    case "specific":
        $result['result'] = search_specific($page, $_GET);
        break;
    case "normal":
        $result['result'] = search_normal($page, explode(' ', $_GET['q']));
        break;
    default:
        $result['success'] = false;
        $result['message'] = 'invalid method';
}
echo json_encode($result);
