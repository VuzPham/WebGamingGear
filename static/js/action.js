let list = document.querySelector('.slider .list');
let items = document.querySelectorAll('.slider .list .item');
let dots = document.querySelectorAll('.slider .dot li');
let prev = document.querySelector('#prev');
let next = document.querySelector('#next');

console.log(items);
let active = 0;
let lengthItems = items.length - 1;
next.onclick = function(){
    if(active + 1 >lengthItems){
        active = 0
    }
    else{
        active += 1;
    }
    reloadSlider();
}
prev.onclick = function(){
    if(active - 1 < 0){
        active = lengthItems;
    }
    else{
        active -= 1;
    }
    reloadSlider();
}
function reloadSlider(){
    let checkLeft = items[active].offsetLeft;
    list.style.left = -checkLeft + 'px';
    
    // let lastActiveDot = document.querySelector()
}
