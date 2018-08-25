<?php
    $conn = mysqli_connect('localhost', 'THE_USERNAME', 'THE_PASSWORD',"THE_DATABASE");
    if(! $conn ) die('Could not connect: ' . mysqli_error());
    $conn->set_charset("utf8");
    header("Content-type: text/html; charset=utf8"); 
    mysqli_query($conn,'set character_set_server=utf8;');
    $curesult = Array();
    $ccities  = Array();
    $cnum  = Array();
    if ($_SERVER["REQUEST_METHOD"] == "GET") {
        $qr = "FROM OI_school WHERE 1=1 ";
        if(isset($_GET["page"])){
            $pg = (int)$_GET["page"];
        }
        else{
            $pg = 1;
        }
		mysql_real_escape_string($_GET["province"]);
		mysql_real_escape_string($_GET["city"]);
        if(isset($_GET["province"]) && $_GET["province"]!="")$qr = $qr." and province = '".$_GET["province"]."'";
        if(isset($_GET["city"]) && $_GET["city"]!="")$qr = $qr." and city = '".$_GET["city"]."'";
        $result = mysqli_query($conn,"SELECT id,name,rating,division,province,city,rank ".$qr." ORDER BY `rating`  DESC LIMIT ".strval($pg*10-10).",10");
        while($row=mysqli_fetch_array($result,MYSQL_ASSOC))array_push($curesult,$row);
        $result = mysqli_query($conn,"SELECT COUNT(*) ".$qr);
        while($row=mysqli_fetch_array($result,MYSQL_ASSOC))array_push($cnum,$row);
        if(isset($_GET["province"]) && $_GET["province"]!=""){
            $result = mysqli_query($conn,"SELECT  city FROM OI_school where province = '".$_GET["province"]."' GROUP BY city order by sum(rating) desc");
            while($row=mysqli_fetch_array($result,MYSQL_ASSOC))array_push($ccities,$row["city"]);
        }
    }
    $count = 0;
    $result = Array();
    $result["result"] = $curesult;
    $result["cities"] = $ccities;
    $result["count"] = $cnum[0]["COUNT(*)"];
    echo json_encode($result);
    mysqli_close($conn);
    ?>
