let selectedCard = null;
let moveObject = null;
let phantomSize = document.getElementById("cell_0_0").offsetWidth;
let halfPhantomSize = phantomSize / 2;

document.addEventListener('click',(event) => {
    let obj = event.target;
    if(obj.className == "player-card-img")
    {
        if(selectedCard ==  null)
        {
            console.log("card selected")
            selectedCard = obj.src;
            console.log(selectedCard);
            createPhantomCard(selectedCard);
        }
    }else if(obj.className == "cell")
    {
        if(selectedCard !=  null)
        {
            console.log("card placed on:");
            console.log(obj);
            selectedCard = null;
        }
    }
    else
    {
        console.log("card deselected");
        selectedCard = null;
    }
});

function createPhantomCard(src)
{
    moveObject = document.createElement("div");
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
            console.log(current_element, x_abs,y_abs);
            moveObject.style.top = (y_abs + halfPhantomSize).toString() + "px";
            moveObject.style.left = (x_abs + halfPhantomSize).toString() + "px";
        }else
        {
            moveObject.style.top= y.toString() + "px";
            moveObject.style.left= x.toString() + "px";
        }
    }
}