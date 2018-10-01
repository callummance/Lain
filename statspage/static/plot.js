~function() {

    var render_speedgraph = function() {
        var target = document.getElementById("speedtest_graph");

        $.get("/api/speedtests.json", (data) => {
            var dates = [];
            var downloads = [];
            var uploads = [];
    
            Object.keys(data).map((key, _) => {
                dates.push(new Date(data[key].time.$date));
                downloads.push(data[key].download);
                uploads.push(data[key].upload);
            });

            var dltrace = {
                type: "scatter",
                mode: "markerslines",
                name: "Download Speeds",
                x: dates,
                y: downloads,
                line: {color: '#17BECF'}
            };

            var ultrace = {
                type: "scatter",
                mode: "markers+lines",
                name: "Upload Speeds",
                x: dates,
                y: uploads,
                line: {color: '#7F7F7F'}
            };

            var min_date = dates.reduce(function (a, b) { return a < b ? a : b; }); 
            var max_date = dates.reduce(function (a, b) { return a > b ? a : b; });

            var data = [dltrace, ultrace];

            var layout = {
                title: "Upload and Download Speeds in bit/s",
                xaxis: {
                    autorange: true,
                    range: [min_date, max_date],
                    rangeselector: {buttons: [
                        {
                            count: 1,
                            label: "1m",
                            step: "month",
                            stepmode: "backward"
                        },
                        {
                            count: 1,
                            label: "1w",
                            step: "week",
                            stepmode: "backward"
                        },
                        {
                            step: "all"
                        }
                    ]},
                    rangeslider: {rangeslider: [min_date, max_date]},
                    type: "date"
                },
                yaxis: {
                    autorange: true,
                    type: "linear"
                }
            };

            Plotly.newPlot("speedtest_graph", data, layout);
        });
    }

    var render_pinggraph = function() {
        var target = document.getElementById("pingtest_graph");

        $.get("/api/pingtests.json", (data) => {
            var dates = [];
            var latencies = []
    
            Object.keys(data).map((key, _) => {
                dates.push(new Date(data[key].time.$date));
                latencies.push(data[key].mean_ping);
            });

            var pings = {
                type: "scatter",
                mode: "markerslines",
                name: "Latency",
                x: dates,
                y: latencies,
                line: {color: '#17BECF'}
            };

            var min_date = dates.reduce(function (a, b) { return a < b ? a : b; }); 
            var max_date = dates.reduce(function (a, b) { return a > b ? a : b; });

            var data = [pings];

            var layout = {
                title: "Latency to Cloudflare DNS servers",
                xaxis: {
                    autorange: true,
                    range: [min_date, max_date],
                    rangeselector: {buttons: [
                        {
                            count: 1,
                            label: "1m",
                            step: "month",
                            stepmode: "backward"
                        },
                        {
                            count: 1,
                            label: "1w",
                            step: "week",
                            stepmode: "backward"
                        },
                        {
                            step: "all"
                        }
                    ]},
                    rangeslider: {rangeslider: [min_date, max_date]},
                    type: "date"
                },
                yaxis: {
                    autorange: true,
                    type: "linear"
                }
            };

            Plotly.newPlot("pingtest_graph", data, layout);
        });
    }

    render_speedgraph();
    render_pinggraph();
}();
