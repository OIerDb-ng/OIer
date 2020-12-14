<?php
	require_once 'dbinfo.php';
    error_reporting(0);
	header("Access-Control-Allow-Origin: http://www.bytew.net, http://xn--vuqs4zq3d.com");
    // $conn = mysqli_connect('localhost', 'THE_USERNAME', 'THE_PASSWORD',"THE_DATABASE");
    $conn = mysqli_connect(DbInfo::HOST, DbInfo::USER, DbInfo::PASSWD, DbInfo::DBNAME);
    if(!$conn) die('Could not connect: ' . mysqli_connect_error());
    $conn->set_charset("utf8");
    header("Content-type: text/html; charset=utf8"); 
    if ($_SERVER["REQUEST_METHOD"] == "GET") {
        $q = (int)$_GET["id"];
        $curesult = Array();
        $result = mysqli_query($conn,"SELECT * FROM OI_school Where id = '$q'");
        while($row=mysqli_fetch_array($result,MYSQLI_ASSOC))array_push($curesult,$row);
    }
    $count = 0;
    $result = Array();
    $result["result"] = $curesult;
    echo json_encode($result);
    mysqli_close($conn);
?>
