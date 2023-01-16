function show_message(message)
{
    alert(message["message"])
}

function update_game_status(message)
{
    if(message["message_type"] == "error")
    {
        show_message(message["message"])
    }else if(message["message_type"] == "game_status_data")
    {
        console.log("fetched game status...")

        var arrows = document.getElementsByClassName("player-panel-turn");
        for (var i = 0; i < arrows.length; i++) {

           arrows[i].style.visibility = "hidden";
        }

        document.getElementById("player_"+message["game_turn"]+"_turn").style.visibility = "visible";

        document.getElementById("player-turn-text").innerHTML = document.getElementById(message["game_turn"]+"_name").innerHTML;

        if(document.getElementById("data-player_id").innerHTML == message["game_turn"])
        {
            document.getElementById("action-panel-end_turn_button").disabled = false;
        }else
        {
            document.getElementById("action-panel-end_turn_button").disabled = true;
        }

    }
    else
    {
        show_message("unexpected error!\nrequest content:\n"+message)
    }
}

function get_request(url, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(JSON.parse(xmlHttp.responseText));
    }
    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.send(null);
}

function end_turn(game_id, player_id)
{
    get_request("/game/end_turn?game_id="+game_id+"&player_id="+player_id, show_message)
}


function fetch_game_status(game_id)
{
    get_request("/game/fetch_game_status?game_id="+game_id, update_game_status)
}

