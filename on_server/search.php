<?php
	header("Access-Control-Allow-Origin: http://www.bytew.net");
	$conn = mysqli_connect('localhost', 'THE_USERNAME', 'THE_PASSWORD',"THE_DATABASE");
	if(! $conn ) die('Could not connect: ' . mysqli_error());
	$conn->set_charset("utf8");
	header("Content-type: text/html; charset=utf8");
	mysqli_query('set character_set_server=utf8;');
	if ($_SERVER["REQUEST_METHOD"] == "GET") {
		$curesult = Array();
		if($_GET["method"] != "specific"){
		    $q = $_GET["q"];
			$orz = split(" ",$_GET["q"]);
			$got = 0;
			foreach($orz as $cui){
				$cui = mysqli_real_escape_string($conn,$cui);
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
			if(isset($_GET["province"])){
				$province = mysqli_real_escape_string($conn,$_GET["province"]);
			}else{
				$province = "";
			}
			if(isset($_GET["pinyin"])){
				$pinyin = mysqli_real_escape_string($conn,$_GET["pinyin"]);
			}else{
				$pinyin = "";
			}
			if(isset($_GET["school"])){
				$school = mysqli_real_escape_string($conn,$_GET["school"]);
			}else{
				$school = "";
			}
			if($pinyin!="")$qustr = $qustr." and pinyin = '".$pinyin."'";
			if($province!="")$qustr = $qustr." and awards like '%".$province."%'";
			if($school!=""){
				$cresult = mysqli_query($conn,"SELECT * FROM OI_school where name like \"%'".$school."'%\"");
				$ccresult = Array();
				while($row=mysqli_fetch_array($cresult,MYSQL_ASSOC)){
					array_push($ccresult,$row);
				}
				if(count($ccresult)==1){
					$qustr = $qustr." and awards like \"%'school_id': ".$ccresult[0]["id"].",%\"";
				}else{
					$qustr = $qustr." and awards like '%".$school."%'";
				}
			}
			if(isset($_GET["name"])){
				$name = mysqli_real_escape_string($conn,$_GET["name"]);
			}else{
				$name = "";
			}
			if($name!="")$qustr = $qustr." and name = '".$name."'";
			$year=intval($_GET["year"]);
			if(isset($_GET["year"]) && $_GET["year"]!="")$qustr = $qustr." and year = $year";
			$result = mysqli_query($conn,$qustr."  LIMIT 0 , 100");
			while($row=mysqli_fetch_array($result,MYSQL_ASSOC)){
				array_push($curesult,$row);
			}
		}
	}
	$count = 0;
	$result = Array();
	if(count($curesult)>100)$curesult = array_slice($curesult,0,100);
	$result["result"] = $curesult;
	echo json_encode($result);
	mysqli_close($conn);
?>
