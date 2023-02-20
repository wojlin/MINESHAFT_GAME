let placeholderObj = null;
let selectedCard = null;
let moveObject = null;
let phantomSize = document.getElementById("cell_0_0_img").offsetWidth;

let phantomPlaceholderSize = document.getElementsByClassName("action-panel-player-cards-table-cell")[0].offsetWidth;

let halfPhantomSize = phantomSize / 2;

let currentCell = null;

moveMade = false;
turnEnd = false;

function showCorrectInfo(message)
{
    if(message["message_type"] == "error")
    {
        document.getElementById("phantomCardTint").style.background = "red"; // colorize red
        show_message(message);
    }
    else if(message["message_type"] == "game_status_data")
    {
        if(message["message"] == true)
        {
            document.getElementById("phantomCardTint").style.background = "green"; // colorize green
        }
        else
        {
            document.getElementById("phantomCardTint").style.background = "red"; // colorize red
        }
    }
    else
    {
        document.getElementById("phantomCardTint").style.background = "red"; // colorize red
        show_message({"message":"unexpected error!\nrequest content:\n"+message});
    }
}

function placeElement(message)
{
    if(message["message_type"] == "error")
    {
        show_message(message);
        return;
    }
    if(message["message_type"] != "game_status_data")
    {
        show_message(message);
        return;
    }

    if(message["message"] != true)
    {
        return;
    }

    moveMade = true;
    document.getElementById("action-panel-end_turn_button").disabled = false;

    let cardInfo = JSON.parse(placeholderObj.dataset.info);

    if(cardInfo['card_type'] == "Tunnel Card")
    {
        playerMove =
        {
         "card": placeholderObj.dataset.info,
         "move_type": "map",
         "move_pos":
             {
                "x": currentCell.id.split("_")[1],
                "y":  currentCell.id.split("_")[2]
             }
         };
    }else if(cardInfo['card_type'] == "Action Card")
    {
        playerMove =
        {
         "card": placeholderObj.dataset.info,
         "move_type": "action",
         "move_action":
             {
                 "desired_player_id": currentCell.dataset.playerid.toString(),
                 "desired_player_action": currentCell.dataset.actionnum.toString()
             }
         };
    }else
    {
    console.log('unexpected card type!');
    }
    removePhantomCard(currentCell);

}

function isMoveCorrect(current_element, place=false)
{
    let card = JSON.parse(placeholderObj.dataset.info);

    let vars = "?";
    vars += "game_id=" + document.getElementById("data-game_id").innerHTML;
    vars += "&player_id=" + document.getElementById("data-player_id").innerHTML;
    vars += "&card=" + placeholderObj.dataset.info + "";
    if(card['card_type'] == 'Tunnel Card' && current_element.classList.contains('cell'))
    {
        vars += "&pos_x=" + current_element.id.split("_")[1];
        vars += "&pos_y=" + current_element.id.split("_")[2];
    }
    else if(card['card_type'] == 'Action Card' && current_element.classList.contains('action_image_dummy'))
    {
        vars += "&desired_player_id=" + current_element.dataset.playerid.toString();
        vars += "&desired_player_action=" + current_element.dataset.actionnum.toString();
    }else
    {
        console.log('incorrect card type');
    }
    if(moveMade)
    {
        document.getElementById("phantomCardTint").style.background = "red";
    }
    else
    {
        if(!place)
        {
            get_request('game/is_move_correct' + vars, showCorrectInfo);
        }else
        {
            get_request('game/is_move_correct' + vars, placeElement);
        }
    }


}

document.addEventListener('click',(event) => {
    let obj = event.target;
    if(obj.className == "player-card-img")
    {
        if(selectedCard ==  null)
        {
            console.log("card selected")
            selectedCard = obj.src;
            obj.src = "";
            console.log(selectedCard);
            createPhantomCard(obj, selectedCard);
        }else
        {
            if(obj.getAttribute('src') == "")
            {
                console.log("placing card back");
                obj.src = selectedCard;
                removePhantomCard(null, force_delete = true)
            }
        }
    }else if(obj.classList.contains("cell_dummy"))
    {
        if(selectedCard !=  null)
        {
            console.log("card placed on cell:");
            console.log(obj);
            isMoveCorrect(obj, true);

        }
    }
    else if(obj.classList.contains("action_image_dummy"))
    {
        if(selectedCard !=  null)
        {
            console.log("card placed on action:");
            console.log(obj);
            isMoveCorrect(obj, true);
        }
    }
     else if(obj.classList.contains("trash_box"))
    {
        if(selectedCard !=  null)
        {
            console.log("card discarded!");

            playerMove =
            {
             "card": placeholderObj.dataset.info,
             "move_type": "trash"
             };

             moveMade = true;
            document.getElementById("action-panel-end_turn_button").disabled = false;

            removePhantomCard(null, force_delete=true);
        }
    }
    else
    {
        if(selectedCard != null)
        {
            console.log("card deselected");
            removePhantomCard(null);
        }

    }
});

function removePhantomCard(placedObj, force_delete = false)
{
    console.log(force_delete)
    document.body.style.setProperty('cursor', 'default');
    if(placedObj == null && force_delete == false)
    {
        placeholderObj.src = selectedCard;
    }
    if(placedObj != null)
    {
        placedObj.src = selectedCard;
    }
    moveObject.remove();
    selectedCard = null;
    placeholderObj = null;
}

function createPhantomCard(obj, src)
{
    placeholderObj = obj;
    moveObject = document.createElement("div");
    let tintObject = document.createElement("div");
    tintObject.id = "phantomCardTint";
    tintObject.classList.add('moveObjectTint');
    tintObject.style.width = "100%";
    tintObject.style.height = "100%";
    moveObject.appendChild(tintObject);
    moveObject.id = "phantomCard";
    moveObject.classList.add('moveObject');
    moveObject.style.background = "url("+src+")";
    moveObject.style.width = phantomSize.toString() + "px";
    moveObject.style.height = phantomSize.toString() + "px";
    document.body.appendChild(moveObject);
}

function cardMove(e)
{
    let x = e.clientX;
    let y = e.clientY;
    if(selectedCard != null)
    {
        let current_element = document.elementFromPoint(x, y);
        if(current_element.classList.contains("cell"))
        {
            let rect = current_element.getBoundingClientRect();
            let x_abs = rect.left + window.scrollX;
            let y_abs = rect.top + window.scrollY;
            moveObject.style.top = (y_abs + halfPhantomSize).toString() + "px";
            moveObject.style.left = (x_abs + halfPhantomSize).toString() + "px";
            moveObject.style.width = phantomSize.toString() + 'px';
            moveObject.style.height = phantomSize.toString() + 'px';
            document.body.style.setProperty('cursor', 'pointer');
            if(currentCell != current_element)
            {
                isMoveCorrect(current_element);
                currentCell = current_element;
            }
        }
        else if(current_element.classList.contains("action_image_dummy"))
        {
            let rect = current_element.getBoundingClientRect();
            let phantomActionSize = document.getElementsByClassName("action_image_dummy")[0].offsetWidth;
            let half = phantomActionSize / 2;
            let x_abs = rect.left + window.scrollX;
            let y_abs = rect.top + window.scrollY;
            moveObject.style.top = (y_abs + half).toString() + "px";
            moveObject.style.left = (x_abs + half).toString() + "px";
            moveObject.style.width = phantomActionSize.toString() + 'px';
            moveObject.style.height = phantomActionSize.toString() + 'px';
            document.body.style.setProperty('cursor', 'pointer');
            if(currentCell != current_element)
            {
                isMoveCorrect(current_element);
                currentCell = current_element;
            }
        }
        else if(current_element.classList.contains("player-card-img"))
        {
            let rect = current_element.getBoundingClientRect();
            let x_abs = rect.left + window.scrollX;
            let y_abs = rect.top + window.scrollY;
            moveObject.style.top = (y_abs + halfPhantomSize).toString() + "px";
            moveObject.style.left = (x_abs + halfPhantomSize).toString() + "px";
            moveObject.style.width = phantomPlaceholderSize.toString() + 'px';
            moveObject.style.height = phantomPlaceholderSize.toString() + 'px';
            document.body.style.setProperty('cursor', 'pointer');
           if( current_element.getAttribute('src')== "")
           {
             document.getElementById("phantomCardTint").style.background = "green";
             console.log("card is moved back on own place");
           }
           else
           {
             document.getElementById("phantomCardTint").style.background = "red";
             console.log("card is badly moved not on it's own place");
           }
        }
        else
        {
            moveObject.style.top= y.toString() + "px";
            moveObject.style.left= x.toString() + "px";
            moveObject.style.width = phantomSize.toString() + 'px';
            moveObject.style.height = phantomSize.toString() + 'px';
            document.body.style.setProperty('cursor', 'default');
        }
    }
}