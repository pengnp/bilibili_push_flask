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
//$('#login').hide();
//$('#tupian').show();
//$('span.today').click(
//    function(){
//       $('#login').toggle()
//       $('#tupian').toggle()
//    }
//);

function lunbo(){
    if(tupian){
        index = Math.floor(Math.random() * img_list.length);
        var img = document.getElementById("tupian");
        img.src = "/static/img/lunbo/"+img_list[index];
        img_list.splice(index, 1);
        if (img_list.length == 0){
            img_list = JSON.parse(data).img
        }
    }
}
//2.定义定时器
setInterval(lunbo, 3000);

document.getElementById('title_新闻').style.backgroundColor="#FFAA33";
function xs(elm){
    document.getElementById('title_'+elm).style.backgroundColor="#FFAA33";
    Array.from(document.getElementsByClassName("news")).forEach(
    function(element, index, array) {
        if(element.getAttribute('id') != elm ){
            element.style.display="none";
            document.getElementById('title_'+element.getAttribute('id')).style.backgroundColor="";
        }
    });
    document.getElementById(elm).style.display="";
}