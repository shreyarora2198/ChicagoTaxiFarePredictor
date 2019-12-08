function getResult() {

    var url = "http://localhost:8000";   // The URL and the port number must match the server-side
    var endpoint = "/result";

    var http = new XMLHttpRequest();
    var trip_seconds = document.getElementById("duration").value;
    var trip_miles = document.getElementById("miles").value;
    var pickup_latitude = document.getElementById("pickup-lat").value;
    var pickup_longitude = document.getElementById("pickup-lon").value;
    var dropoff_latitude = document.getElementById("dropoff-lat").value;
    var dropoff_longitude = document.getElementById("dropoff-lon").value;
    var time = document.getElementById("time").value;
    var date = document.getElementById("date").value;
    
    var payload = {"trip_seconds": trip_seconds,
                    "trip_miles": trip_miles,
                    "pickup_latitude": pickup_latitude
                    "pickup_longitude": pickup_longitude
                    "dropoff_latitude": dropoff_latitude
                    "dropoff_longitude": dropoff_longitude
                    "time": time
                    "date": date};
    // JSON string to post
    var payloadString = JSON.stringify(payload);
    http.open("GET", url+endpoint, true);
    	
	
	

  //  http.onreadystatechange = function() {
   //     var DONE = 4;       // 4 means the request is done.
     //   var OK = 200;       // 200 means a successful return.
       // if (http.readyState == DONE && http.status == OK && http.responseText) {

            // JSON string
         //   replyString = http.responseText;

            // turn JSON string into JavaScript object
           // replyObj = JSON.parse(replyString);

           // document.getElementById("result").innerHTML = "JSON received: " + replyString;

     //   }
 //   };

    // Send request
    http.send(payloadString);

}