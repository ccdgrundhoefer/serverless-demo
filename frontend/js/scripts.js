$("#initdb").click(function () { $.get("http://api-create-serverless-demo.apps.cluster-598a.598a.sandbox502.opentlc.com/initdb"); });

$("#refresh").click(function () {
    $.get("http://api-read-serverless-demo.apps.cluster-598a.598a.sandbox502.opentlc.com", function (data) {

        d = $.parseJSON(data);

        console.log(d);

        $("#temp").html(d.temperature + "°C");
        $("#humidity").html(d.humidity + "%");

        var currentdate = new Date();

        $("#tempfooter").html(d.timestamp);
        $("#humfooter").html(d.timestamp);
    });

    $.get("http://api-read-serverless-demo.apps.cluster-598a.598a.sandbox502.opentlc.com/chart", function (data) {

        d = $.parseJSON(data);

        const chartdata = {
            datasets: [{
                label: 'Temperature',
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                data: d.temp,
                tension: 0.1
            }]
        };

        const config = {
            type: 'line',
            chartdata,
        };

        var tempChart = new Chart(
            document.getElementById('tempchart'),
            config
        );
    });
});