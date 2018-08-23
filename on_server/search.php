<?php
	$conn = mysqli_connect('localhost', 'THE_USERNAME', 'THE_PASSWORD',"THE_DATABASE");
	if(! $conn ) die('Could not connect: ' . mysqli_error());
	$conn->set_charset("utf8");
	header("Content-type: text/html; charset=utf8");
	mysqli_query('set character_set_server=utf8;');
	if ($_SERVER["REQUEST_METHOD"] == "GET") {
		$curesult = Array();
		if($_GET["method"] != "specific"){
			mysql_real_escape_string($_GET["q"]);
			$q = $_GET["q"];
			$orz = split(" ",$q);
			$got = 0;
			foreach($orz as $cui){
				if(count($curesult)==0){
					if(preg_match("/^[a-zA-Z\s]+$/",$cui)){
						if(count($newresult)) continue;
						$curi = strtolower($cui);
						$result = mysqli_query($conn,"SELECT * FROM OIers Where pinyin = '$curi'");
						while($row=mysqli_fetch_array($result,MYSQL_ASSOC)){
							array_push($curesult,$row);
						}
					}else{
						$result = mysqli_query($conn,"SELECT * FROM OIers Where name = '$cui'");
						while($row=mysqli_fetch_array($result,MYSQL_ASSOC)){
							array_push($curesult,$row);
						}
						if(!count($newresult)){
							$result = mysqli_query($conn,"SELECT * FROM OIers Where awards like '%$cui%'");
							while($row=mysqli_fetch_array($result,MYSQL_ASSOC)){
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
		}else{
			$qustr = "SELECT * FROM OIers Where 1 = 1 ";
			if(isset($_GET["pinyin"]) && $_GET["pinyin"]!="")$qustr = $qustr." and pinyin = '".$_GET["pinyin"]."'";
			if(isset($_GET["province"]) && $_GET["province"]!="")$qustr = $qustr." and awards like '%".$_GET["province"]."%'";
			if(isset($_GET["school"]) && $_GET["school"]!="")$qustr = $qustr." and awards like '%".$_GET["school"]."%'";
			if(isset($_GET["name"]) && $_GET["name"]!="")$qustr = $qustr." and name = '".$_GET["name"]."'";
			//echo $qustr."  LIMIT 0 , 60";
			$result = mysqli_query($conn,$qustr."  LIMIT 0 , 60");
			while($row=mysqli_fetch_array($result,MYSQL_ASSOC)){
				array_push($curesult,$row);
			}
		}
	}
	$count = 0;
	$result = Array();
	if(count($curesult)>60)$curesult = array_slice($curesult,0,60);
	$result["result"] = $curesult;
	echo json_encode($result);
	mysqli_close($conn);
?>
