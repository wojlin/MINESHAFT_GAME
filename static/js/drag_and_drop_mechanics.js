let placeholderObj = null;
let selectedCard = null;
let moveObject = null;
let phantomSize = document.getElementById("cell_0_0_img").offsetWidth;
let phantomActionSize = document.getElementsByClassName("action_image_dummy")[0].offsetWidth;
let phantomPlaceholderSize = document.getElementsByClassName("action-panel-player-cards-table-cell")[0].offsetWidth;

let halfPhantomSize = phantomSize / 2;

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
        }
    }else if(obj.classList.contains("cell_dummy"))
    {
        if(selectedCard !=  null)
        {
            console.log("card placed on cell:");
            console.log(obj);
            removePhantomCard(obj);
        }
    }
    else if(obj.classList.contains("action_image_dummy"))
    {
        if(selectedCard !=  null)
        {
            console.log("card placed on action:");
            console.log(obj);
            removePhantomCard(obj);
        }
    }
     else if(obj.classList.contains("trash_box"))
    {
        if(selectedCard !=  null)
        {
            console.log("card discarded!");
            removePhantomCard(null, force_delete=true);
        }
    }
    else
    {
        console.log("card deselected");
        removePhantomCard(null);
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
        }
        else if(current_element.classList.contains("action_image_dummy"))
        {
            let rect = current_element.getBoundingClientRect();
            let x_abs = rect.left + window.scrollX;
            let y_abs = rect.top + window.scrollY;
            moveObject.style.top = (y_abs + halfPhantomSize).toString() + "px";
            moveObject.style.left = (x_abs + halfPhantomSize).toString() + "px";
            moveObject.style.width = phantomActionSize.toString() + 'px';
            moveObject.style.height = phantomActionSize.toString() + 'px';
            document.body.style.setProperty('cursor', 'pointer');
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