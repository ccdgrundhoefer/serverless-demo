$("#initdb").get("http://api-create-serverless-demo.apps.cluster-598a.598a.sandbox502.opentlc.com/initdb");
$("#refresh").click(function() {
    $.get("http://api-read-serverless-demo.apps.cluster-598a.598a.sandbox502.opentlc.com", function (data) {
        
        d = $.parseJSON(data);
        
        console.log(d);

        $("#temp").html(d.temperature + "°C");
        $("#humidity").html(d.humidity + "%");

        var currentdate = new Date();

        $("#tempfooter").html(currentdate.getHours() + ":" + currentdate.getMinutes() + ":" + currentdate.getSeconds());
        $("#humfooter").html(currentdate.getHours() + ":" + currentdate.getMinutes() + ":" + currentdate.getSeconds());
    });
});