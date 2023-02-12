function get_request(url, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        {
            let json = JSON.parse(xmlHttp.responseText);
            callback(json);
        }

    }
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}

function fetch_stats_handler(stats)
{
    document.getElementById("total_memory").innerHTML = stats["total_memory"];
    document.getElementById("start_time").innerHTML = stats["start_time"];
    document.getElementById("elapsed_time").innerHTML = stats["elapsed_time"];
    document.getElementById("rooms_amount").innerHTML = stats["rooms_amount"];
    document.getElementById("rooms_memory").innerHTML = stats["all_rooms_memory"];
    document.getElementById("games_amount").innerHTML = stats["games_amount"];
    document.getElementById("games_memory").innerHTML = stats["all_games_memory"];
    document.getElementById("rpm").innerHTML = stats["rpm"];

    let rooms_table = document.getElementById("rooms_table").querySelector("tbody");
    let count = 1;
    rooms_table.innerHTML = '';
    for (const [key, value] of Object.entries(stats["rooms_memory"]))
    {
        let html = "<tr>" +
            "<td>"+count.toString()+"</td>" +
            "<td>"+key+"</td>" +
            "<td>"+value+"</td>" +
            "</tr>";
        rooms_table.innerHTML += html;
        count++;
    }

    let games_table = document.getElementById("games_table").querySelector("tbody");
    count = 1;
    games_table.innerHTML = '';
    for (const [key, value] of Object.entries(stats["games_memory"]))
    {
        let html = "<tr>" +
            "<td>"+count.toString()+"</td>" +
            "<td>"+key+"</td>" +
            "<td>"+value+"</td>" +
            "</tr>";
        games_table.innerHTML += html;
        count++;
    }

    let xValues = stats["plot_x"];
    let yValues = stats["plot_y"];
    let y1Values = stats["plot_rpm"];

    new Chart("myChart", {
      type: "line",
      data:
      {
        labels: xValues,
        datasets:
        [
            {
                label: 'RAM usage',
                data: yValues,
                borderColor: "rgba(255,0,0,1)",
                backgroundColor: "rgba(255,0,0,0.1)",
                yAxisID: 'y'
            },
            {
                label: 'requests per minute',
                data: y1Values,
                borderColor: "rgba(255,255,0,1)",
                backgroundColor: "rgba(255,0,0,0.0)",
                yAxisID: 'y1'
            }
        ]
      },
      options:
      {
        animation: false,
        tooltips:
        {
            enabled: false
        },
        legend:
        {
            display: false
        },
        elements:
        {
            point:
            {
                radius: 0
            }
        },
        scales:
        {
            yAxes:
            [
                {
                    id: 'y',
                    position: 'left',
                    type: 'linear',
                    ticks:
                    {
                        userCallback: function(item)
                        {
                            return item + " MB";
                        },
                    }
                },
                {
                    id: 'y1',
                    position: 'right',
                    type: 'linear',
                    ticks:
                    {
                        userCallback: function(item)
                        {
                            return item + " RPM";
                        },
                    },
                    gridLines:
                    {
                        color: "rgba(0, 0, 0, 0)",
                    }
                }
            ]
        }
      }
    });
}


function fetch_stats()
{
    get_request("/stats/fetch_stats", fetch_stats_handler)
}

setInterval(function(){fetch_stats()}, 1000);