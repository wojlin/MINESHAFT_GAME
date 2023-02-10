var counter = 30;

function decreaseCount()
{
    if(counter <= 0)
    {
        if(document.body.dataset.round < 3)
        {
            window.location.href = "/game?game_id=" + document.body.dataset.gameid + "&player_id=" + document.body.dataset.playerid;
        }
        else
        {
            window.location.href = "/game/leaderboard?game_id=" + document.body.dataset.gameid;
        }
    }
    counter--;
    document.getElementById("counter").innerHTML = counter.toString();
}

const interval = setInterval(function() {
   decreaseCount();
 }, 1000);

function dispose_rank(player)
{

    let dest_obj = document.getElementById(player["player_id"]+ "_rank");
    let dest_text = document.getElementById(player["player_id"]+ "_text");
    let dest_rect = dest_obj.getBoundingClientRect();

    let destination_x = dest_rect.left + window.scrollX;
    let destination_y = dest_rect.top + window.scrollY;
    console.log(destination_x, destination_y);



    let purse = document.getElementById("purse").getBoundingClientRect();
    let purse_pos_x = purse.left + window.scrollX;
    let purse_pos_y = purse.top + window.scrollY;
    let purse_width = purse.width / 4;
    let purse_height = purse.height / 4;
    let img = document.createElement("img");
    img.src = player["rank_url"];
    img.alt = "";
    img.classList.add("rank_animated");
    img.style.top =  (purse_pos_y - purse_height).toString() + "px";
    img.style.left =  (purse_pos_x + purse_width).toString() + "px";
    img.style.setProperty('--rank_x', destination_x.toString()+'px');
    img.style.setProperty('--rank_y', destination_y.toString()+'px');
    document.body.appendChild(img);




    setTimeout(function() {img.style.display = 'none';dest_obj.src = player["rank_url"];dest_text.innerHTML=player["rank"];}, 1000);

}

function dispose_ranks()
{
    let data = JSON.parse(document.body.dataset.players_data);
    console.log(data);

    let i = 0;
    for(let key in data)
    {
        let player = data[key];
        if(player["rank"] != player["last_player_rank"])
        {
            setTimeout(function() {dispose_rank(player)}, i*1200);
            i++;
        }
    }
}

dispose_ranks();