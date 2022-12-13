tupian = true
var data = document.getElementById('dataid').getAttribute('d');
var img_list = JSON.parse(data).img;
document.getElementById('login').style.display="none";

Array.from(document.getElementsByClassName("news")).forEach(
    function(element, index, array) {
        if(index != 0){
            element.style.display="none";
        }
});

function login(){
    document.getElementById('login').style.display="";
    document.getElementById('tupian').style.display="none";
    tupian = false
}

function lunbo(){
    if(tupian){
        index = Math.floor(Math.random() * img_list.length);
        var img = document.getElementById("tupian");
        img.src = "/static/img/"+img_list[index];
        console.log(index)
    }
}
//2.定义定时器
setInterval(lunbo, 3000);

function xs(elm){
    Array.from(document.getElementsByClassName("news")).forEach(
    function(element, index, array) {
        if(element.getAttribute('id') != 'elm' ){
            element.style.display="none";
        }
    });
    document.getElementById(elm).style.display="";
}