function getResult() {

    var url = "http://localhost:8000";   // The URL and the port number must match the server-side
    var endpoint = "/result";

    var http = new XMLHttpRequest();

    http.open("GET", url+endpoint, true);

    http.onreadystatechange = function() {
        var DONE = 4;       // 4 means the request is done.
        var OK = 200;       // 200 means a successful return.
        if (http.readyState == DONE && http.status == OK && http.responseText) {

            // JSON string
            replyString = http.responseText;

            // turn JSON string into JavaScript object
            replyObj = JSON.parse(replyString);

            document.getElementById("result").innerHTML = "JSON received: " + replyString;

        }
    };

    // Send request
    http.send();

}