$("#initdb").get("http://api-create-serverless-demo.apps.cluster-598a.598a.sandbox502.opentlc.com/initdb");
$("#refresh").click(function() {
    $.get("http://api-read-serverless-demo.apps.cluster-598a.598a.sandbox502.opentlc.com", function (data) {
        $("#temp").html(data)

        var currentdate = new Date();

        $("#tempfooter").html(currentdate.getHours() + ":" + currentdate.getMinutes + ":" + currentdate.getSeconds())
    });
});