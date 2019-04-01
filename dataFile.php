<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

$conn = new mysqli("149.144.241.103", "rasp", "pi", "ITPCarPark");

$result_old = $conn->query("select A.CarParkID,A.CarParkName,A.TotalCapacity,B.SlotsAvailable,C.Classifications from CarParks A join CarParkData B on A.CarParkID=B.CarParkID,B.CarParkID=C.CarParkID;");


$result = $conn->query("select A.CarParkID,A.CarParkName,A.TotalCapacity,B.SlotsAvailable,C.Classifications 
from CarParks A 
join CarParkData B on A.CarParkID=B.CarParkID
join ClassificationData C on B.CarParkID=C.CarParkID
where C.ID in (select max(D.ID) from ClassificationData D);");


$outp = "";
while($rs = $result->fetch_array(MYSQLI_ASSOC)) {
    if ($outp != "") {$outp .= ",";}
    $outp .= '{"carparkID":"'  . $rs["CarParkID"] . '",';
	$outp .= '"carparkName":"'  . $rs["CarParkName"] . '",';
	$outp .= '"totalCapacity":"'  . $rs["TotalCapacity"] . '",';
	$outp .= '"lastClassification":"'  . $rs["Classifications"] . '",';
    $outp .= '"slotsAvailable":"'   . $rs["SlotsAvailable"]        . '"}';
}
$outp ='{"records":['.$outp.']}';
$conn->close();

echo($outp);
?>