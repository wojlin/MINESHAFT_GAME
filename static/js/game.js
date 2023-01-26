var playerMove = ""

function show_message(message)
{
    alert(message["message"])
}

function update_game_status(message)
{
    if(message["message_type"] == "error")
    {
        show_message(message)
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
            let cards = document.getElementsByClassName("action-panel-player-cards-table-cell");
            for (var i = 0; i < cards.length; i++) {
              cards[i].classList.remove("move_disabled");
            }
        }else
        {
            let cards = document.getElementsByClassName("action-panel-player-cards-table-cell");
            for (var i = 0; i < cards.length; i++) {
              cards[i].classList.add("move_disabled");
            }
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

        let cells = document.getElementsByClassName("cell_img");
        Array.prototype.forEach.call(cells, function(cell) {
            cell_id = cell.id;
            cell_x = parseInt(cell_id.split('_')[1]);
            cell_y = parseInt(cell_id.split('_')[2]);
            cell.src = "static/images/" + message['board'][cell_y][cell_x];
        });

        if(turnEnd == true)
        {
            let cards = document.getElementsByClassName("player-card-img");

            for( let i =0; i<cards.length; i++)
            {
                cards[i].src = "-";
                cards[i].dataset.info = "";
            }

            let cards_in_player_stack = [];

            Object.keys( message["player_cards"]).forEach(function(key)
            {
                let card_info = message["player_cards"][key];

                cards_in_player_stack.push(card_info);


            });



            for( let i =0; i<cards_in_player_stack.length; i++)
            {
                cards[i].src = "static/images/" + cards_in_player_stack[i]["card_url"];
                cards[i].dataset.info = JSON.stringify(cards_in_player_stack[i]);
            }
            turnEnd = false;
        }




    }
    else
    {
        show_message({"message":"unexpected error!\nrequest content:\n"+message})
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
    vars = "?game_id=" + game_id;
    vars += "&player_id=" + player_id;
    vars += "&player_move=" + JSON.stringify(playerMove) + "";
    get_request("/game/end_turn"+vars, show_message);
    turnEnd = true;
}


function fetch_game_status(game_id, player_id)
{
    get_request("/game/fetch_game_status?game_id="+game_id+"&player_id="+player_id, update_game_status)
}

//fetch_game_status(document.getElementById("data-game_id").innerHTML);

