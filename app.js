var app = angular.module('myApp', []);

app.controller('carparkData', function($scope, $http,$interval,$timeout) {
	//$scope.map = false;
	 $scope.reload = function () {
        $http.get('dataFile.php').
            then(function (response) {
            console.log('Data Received from server');
			$scope.data = response.data.records;
			console.log($scope.data);
            });
    };
    $scope.reload();
    $interval($scope.reload, 10000);

//	$scope.showMap=function(){
//		$scope.map = true;
//		var myCenter = new google.maps.LatLng(-37.721009,145.054611);
//		var mapProp = {center:myCenter, zoom:15, scrollwheel:false, draggable:true, mapTypeId:google.maps.MapTypeId.ROADMAP};
//		var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
//		var marker = new google.maps.Marker({position:myCenter});
//		marker.setMap(map);
//		var newDirective = angular.element('<div d2>hahahah</div>');
//		element.append(newDirective);
//		$compile(newDirective)($scope);
//	}
//	
//	$scope.hideMap=function(){
//		$scope.map = true;
//		console.log("press");
//	}
	
});