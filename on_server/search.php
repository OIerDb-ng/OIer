<?php
    $conn = mysqli_connect('localhost', 'USER_NAME', 'USER_PASSWORD',"OIer");
    if(! $conn ) die('Could not connect: ' . mysqli_error());
    $conn->set_charset("utf8");
    header("Content-type: text/html; charset=utf8"); 
    mysqli_query($conn,'set character_set_server=utf8;');
    if ($_SERVER["REQUEST_METHOD"] == "GET") {
        $q = $_GET["q"];
        $orz = explode(" ",$q);
        $got = 0;
        $curesult = Array();
        foreach($orz as $cui){
            if(count($curesult)==0){
                if(preg_match("/^[a-zA-Z\s]+$/",$cui)){
                    if(count($newresult)) continue;
                    $curi = strtolower($cui);
                    $result = mysqli_query($conn,"SELECT * FROM OIers Where pinyin = '$curi' LIMIT 0 , 30");
                    while($row=mysqli_fetch_array($result,1)){
                        array_push($curesult,$row);
                    }
                }else{
                    $result = mysqli_query($conn,"SELECT * FROM OIers Where name = '$cui' LIMIT 0 , 30");
                    while($row=mysqli_fetch_array($result,1)){
                        array_push($curesult,$row);
                    }
                    if(!count($newresult)){
                        $result = mysqli_query($conn,"SELECT * FROM OIers Where awards like '%$cui%' LIMIT 0 , 30");
                        while($row=mysqli_fetch_array($result,1)){
                            array_push($curesult,$row);
                        }
                    }
                }
            }else{
                $newresult = Array();
                foreach($curesult as $row){
                    if(strpos ( $row["awards"] ,  $cui )||$row["name"] == $cui ||$row["pinyin"] == $cui )
                        array_push($newresult,$row);
                }
                if(count($newresult)) $curesult = $newresult;
            }
        }
    }
    
    $result = Array();
    $result["result"] = $curesult;
    echo json_encode($result);
    mysqli_close($conn);
    ?>