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
 }, 10000);


function dispose_ranks()
{
    let data = JSON.parse(document.body.dataset.players_data);
    console.log(data);


}

dispose_ranks();