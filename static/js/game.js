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
        //console.log("fetched game status...")

        let arrows = document.getElementsByClassName("player-panel-turn");
        for (var i = 0; i < arrows.length; i++) {

           arrows[i].style.visibility = "hidden";
        }

        document.getElementById("players_"+message["game_turn"]+"_turn").style.visibility = "visible";

        document.getElementById("action-panel-cards_deck-cards_left_text").innerHTML = message["cards_left"];

        document.getElementById("player-turn-text").innerHTML = document.getElementById(message["game_turn"]+"_name").innerHTML;

        document.getElementById("action-panel-round_panel-round_text").innerHTML = message['game_round']

        if(document.getElementById("data-player_id").innerHTML == message["game_turn"])
        {
            document.getElementById("action-panel-end_turn_button").disabled = false;
        }else
        {
            document.getElementById("action-panel-end_turn_button").disabled = true;
        }

        let players_actions = document.getElementsByClassName("action_image");
        for (var i = 0; i < players_actions.length; i++)
        {
            let player_id = players_actions[i].dataset.actionid;
            let action_num = players_actions[i].dataset.actionnum;
            let state = message['players_actions'][player_id][action_num];
            let exp = 'static/images/';

            if(state == true)
            {
                exp += action_num.toString() + "_positive.png";
            }else
            {
                exp += action_num.toString() + "_negative.png";
            }

            players_actions[i].src = exp;
        }

    }
    else
    {
        show_message("unexpected error!\nrequest content:\n"+message)
    }
}

function get_request(url, callback)
{
    let xmlHttp = new XMLHttpRequest();
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

