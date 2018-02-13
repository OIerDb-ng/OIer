<?php
$conn = mysqli_connect('localhost', 'bytewijk', 'W@ng_2025',"bytewijk_OIer");
if(! $conn )
{
    die('Could not connect: ' . mysqli_error());
}
$conn->set_charset("utf8");
header("Content-type: text/html; charset=utf8"); 
mysqli_query('set character_set_server=utf8;');
if ($_SERVER["REQUEST_METHOD"] == "GET") {
  $q = $_GET["q"];
  $orz = split(" ",$q);
  $got = 0;
  $curesult = Array();
  foreach($orz as $cui){
    if(preg_match("/^[a-zA-Z\s]+$/",$cui)){
      if(count($newresult)) continue;
      $curi = strtolower($cui);
      $result = mysqli_query($conn,"SELECT * FROM OIers Where pinyin = '$curi'");
      while($row=mysqli_fetch_array($result)){
        array_push($curesult,$row);
      }
    }else{
      if(count($newresult)){
        $newresult = Array();
        foreach($curesult as $row){
          if(strpos ( $row["awards"] ,  $cui )||strpos ( $row["name"] ,  $cui )||strpos ( $row["pinyin"] ,  $cui ))  {
             array_push($newresult,$row);
          }
        }
        if(count($newresult)) {
           $curesult = $newresult;
        }
      }else{
        $result = mysqli_query($conn,"SELECT * FROM OIers Where name = '$cui'");
        while($row=mysqli_fetch_array($result)){
          array_push($curesult,$row);
        }
        if(!count($newresult)){
          $result = mysqli_query($conn,"SELECT * FROM OIers Where awards like '%$cui%'");
            while($row=mysqli_fetch_array($result)){
            array_push($curesult,$row);
          }
        }
      }
    }
  }
}
foreach($curesult as $row){
    echo $row["id"]."\t".$row["name"]."\t".$row["awards"]."\t".$row["sex"]."\t".$row["year"];
    echo "<br/>";
}
mysqli_close($conn);



?>
