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

function showMessage(message)
{
    alert(message);
}

function fetch_room_handler(data)
{
    console.log(data);
    let player_id = document.body.dataset.playerid;
    if (data["data"]["host_id"] == player_id)
    {
        if(data["data"]["players_amount"] >= 3)
        {
            document.getElementById("start_game").disabled = false;
        }
        else
        {
            document.getElementById("start_game").disabled = true;
        }
    }

    let player_list = document.getElementById("players-list");

    player_list.innerHTML = "";

    let count = 1;
    for (const [key, value] of Object.entries(data["data"]["players"]))
    {
        let entry = document.createElement("li");
        entry.classList.add("player-list-element");
        entry.innerHTML = count.toString() + ". " + value;
        player_list.appendChild(entry);
        count += 1;
    }
    let count_set = count;
    for(let x = 0; x <= 10 - count_set; x++)
    {
        let entry = document.createElement("li");
        entry.classList.add("player-list-element");
        entry.innerHTML = count.toString() + ". " + '-';
        player_list.appendChild(entry);
        count += 1;
    }
}

function fetch_room_status()
{
    let room_id = document.body.dataset.roomid;
    get_request('/room/fetch_room_status?room_id='+room_id, fetch_room_handler);
}

function start_game()
{
    let room = JSON.parse(document.body.dataset.room);
    let player_id = document.body.dataset.playerid;
    let room_id = document.body.dataset.roomid;

    if(room["host_id"] != player_id)
    {
        showMessage("you are not host of the game!");
        return;
    }

    if(room["players_amount"] < 3)
    {
        showMessage("not enough players");
        return;
    }

     get_request('/room/start_game', fetch_start_game_handler)

}


setInterval(function(){fetch_room_status()}, 1000);