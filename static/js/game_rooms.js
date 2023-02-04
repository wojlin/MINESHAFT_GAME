


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
    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.send(null);
}



function create_new_room()
{
    let player_name = document.getElementById("create-player").value;
    let room_name = document.getElementById("create-name").value;
    let room_comment = document.getElementById("create-comment").value;
    let room_password = document.getElementById("create-password").value;
    let url = '/create_room';
    url += "?player_name=" + player_name;
    url += "&room_name=" + room_name;
    url += "&room_comment=" + room_comment;
    url += "&room_password=" + room_password;
    get_request(url, create_new_room_handler)
    console.log("created new room!");

}

function create_new_room_handler(response)
{
    console.log(response)
    window.location.href = '/room?room_id='+response["data"]["room_id"]+"&player_id="+response["data"]["player_id"];
}

function join_room_handler(response)
{
    console.log(response)
    window.location.href = '/room?room_id='+response["data"]["room_id"]+"&player_id="+response["data"]["player_id"];
}


function join_room()
{
    let player_name = document.getElementById("join-player").value;
    let room_id = document.getElementById("join-id").value;
    let room_password = document.getElementById("join-password").value;
    let url = '/join_room';
    url += "?player_name=" + player_name;
    url += "&room_id=" + room_id;
    url += "&room_password=" + room_password;
    get_request(url, join_room_handler)
    console.log("joined room!");
}


document.getElementById('create-password').disabled = !this.checked;
document.getElementById('create-private').onchange = function() {
    document.getElementById('create-password').disabled = !this.checked;
};


function show_join_room_form(room_id, isLocked)
{
    console.log("showing 'join room' form...");
    document.getElementById("join-password").value = "";
    document.getElementById("join-id").value = "";
    if(isLocked == 'false')
    {
        document.getElementById("join-password").style.display = "none";
        document.getElementById("join-password-label").style.display = "none";
    }else
    {
        document.getElementById("join-password").style.display = "block";
        document.getElementById("join-password-label").style.display = "block";
    }
    document.getElementById("join-id").value = room_id;

    document.getElementById('create_new_room_div').style.visibility = 'hidden';
    document.getElementById('join_room_div').style.visibility = 'visible';
    document.getElementById('opacity-div').style.visibility = 'visible';
}

function show_create_new_room_form()
{
    console.log("showing 'create new room' form...");
    document.getElementById('create_new_room_div').style.visibility = 'visible';
    document.getElementById('opacity-div').style.visibility = 'visible';
}

function hide_forms()
{
    document.getElementById('create_new_room_div').style.visibility = 'hidden';
    document.getElementById('join_room_div').style.visibility = 'hidden';
    document.getElementById('opacity-div').style.visibility = 'hidden';
}

function fetch_rooms_status_handler(data)
{
    console.log(data);
    let content = document.querySelector("tbody");
    content.innerHTML = '';

    for (const [key, value] of Object.entries(data["data"]))
    {
        let html = "<tr data-locked='"+value['locked']+"'>" +
            "<td>"+value["room_name"]+"</td>" +
            "<td>"+value["players_amount"]+"/10</td>" +
            "<td>"+value["room_comment"]+"</td>" +
            "<td>";
        if(value["locked"])
        {
            html += "<img src='static/images/locked.png'/>";
        }
        else
        {
            html += "<img src='static/images/unlocked.png'/>";
        }

        html += "</td>" +
            "<td>" +
            "<button onclick='show_join_room_form(\""+value["room_id"]+"\", \""+value["locked"]+"\");' class='join_button'>join</button>" +
            "</td>" +
            "</tr>";
        content.innerHTML += html;
    }
}

function fetch_rooms_status()
{
    get_request("/fetch_rooms_status", fetch_rooms_status_handler);
}

setInterval(function(){fetch_rooms_status()}, 5000);