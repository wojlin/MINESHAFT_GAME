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

function fetch_room_handler(message)
{
    console.log(message);
}

function fetch_room_status()
{
    get_request('/fetch_room_status/', fetch_room_handler)
}

function start_game()
{
    let room = JSON.parse(document.body.dataset.room.value);
    let player_id = JSON.parse(document.body.dataset.playerid.value);
    let room_id = JSON.parse(document.body.dataset.roomid.value);

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

     get_request('/start_game/', fetch_start_game_handler)

}