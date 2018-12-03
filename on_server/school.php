<?php
	header("Access-Control-Allow-Origin: http://www.bytew.net");
    $conn = mysqli_connect('localhost', 'THE_USERNAME', 'THE_PASSWORD',"THE_DATABASE");
    if(! $conn ) die('Could not connect: ' . mysqli_error());
    $conn->set_charset("utf8");
    header("Content-type: text/html; charset=utf8"); 
    mysqli_query('set character_set_server=utf8;');
    if ($_SERVER["REQUEST_METHOD"] == "GET") {
        $q = (int)$_GET["id"];
        $curesult = Array();
        $result = mysqli_query($conn,"SELECT * FROM OI_school Where id = '$q'");
        while($row=mysqli_fetch_array($result,MYSQL_ASSOC))array_push($curesult,$row);
    }
    $count = 0;
    $result = Array();
    $result["result"] = $curesult;
    echo json_encode($result);
    mysqli_close($conn);
?>
