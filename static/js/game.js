var playerMove = ""

function show_message(message)
{
    document.getElementById("popup").style.display = "block";
    document.getElementById("popup-message-title").innerHTML = message["message_type"];
    document.getElementById("popup-message-content").innerHTML = message["message"];
}

function update_game_status(message)
{
    if(message["message_type"] == "error")
    {
        show_message(message)
    }else if(message["message_type"] == "game_status_data")
    {
        //console.log("fetched game status...")
        //console.log(message)



        let arrows = document.getElementsByClassName("players-panel_turn");
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
            let exp = '/load_image?filename=';

            if(state == true)
            {
                exp += action_num.toString() + "_positive.png";
            }else
            {
                exp += action_num.toString() + "_negative.png";
            }

            players_actions[i].src = exp;
        }


        let players_rank_img = document.getElementsByClassName("player_rank_img");
        for (var i = 0; i < players_rank_img.length; i++)
        {
            let player_id = players_rank_img[i].dataset.playerid;
            players_rank_img[i].src = message["players_ranks"][player_id]["rank_url"];
        }

        let players_rank = document.getElementsByClassName("player_rank");
        for (var i = 0; i < players_rank.length; i++)
        {
            let player_id = players_rank[i].dataset.playerid;
            players_rank[i].innerHTML = message["players_ranks"][player_id]["rank"];
        }

        let cells = document.getElementsByClassName("cell_img");
        Array.prototype.forEach.call(cells, function(cell) {
            cell_id = cell.id;
            cell_x = parseInt(cell_id.split('_')[1]);
            cell_y = parseInt(cell_id.split('_')[2]);
            cell.src =  message['board'][cell_y][cell_x];
             cell.src =  cell.src;
        });

        if(turnEnd == true)
        {
            window.location.reload();
            // delete rest
            let cards = document.getElementsByClassName("player-card-img");

            let cardHolders = {};
            let playerCards = message["player_cards"];

            for( let i =0; i<cards.length; i++)
            {
                cardHolders[cards[i].dataset.index.toString()] = cards[i];
            }
            console.log(cards.length)
            console.log(cardHolders);

            console.log(playerCards);

            for (const [key, value] of Object.entries(cardHolders)) {
                 for (const [key1, value1] of Object.entries(playerCards))
                 {
                  if(key.toString() == key1.toString())
                  {
                    console.log('updated card slot n', key, ' with: ', value1["card_url"])
                    cardHolders[key.toString()].src = "/load_image?filename=" + value1["card_url"];
                    cardHolders[key.toString()].dataset.info = JSON.stringify(value1);
                  }
                }
            }

            turnEnd = false;
        }


        if(message["round_ended"] == true)
        {
            let game_id = document.getElementById("data-game_id").innerHTML;
            let player_id = document.getElementById("data-player_id").innerHTML;
            setTimeout(() => { window.location.href = "/game/round_end?game_id=" + game_id + "&player_id=" + player_id; }, 2000);

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
    if(moveMade)
    {
        vars = "?game_id=" + game_id;
        vars += "&player_id=" + player_id;
        vars += "&player_move=" + JSON.stringify(playerMove) + "";
        get_request("/game/end_turn"+vars, show_message);
        turnEnd = true;
    }
    else
    {
        show_message({"message_type": "info", "message": "you need to make move before ending turn"});
    }

}


function fetch_game_status(game_id, player_id)
{
    get_request("/game/fetch_game_status?game_id="+game_id+"&player_id="+player_id, update_game_status)
}

//fetch_game_status(document.getElementById("data-game_id").innerHTML);

