document.getElementById('cover').style.display="none";
function update(user_name, user_email, push, check, update){
    document.getElementById('cover').style.display="";
    document.getElementById('cover_box_update').style.display="";
    document.getElementById('cover_box_add').style.display="none";
    document.getElementById('user_name').setAttribute('value', user_name);
    document.getElementById('user_email').setAttribute('value', user_email);
    if(push == '否'){
        document.getElementById('push').options[1].setAttribute('selected', 'selected');
    }else{
        document.getElementById('push').options[0].setAttribute('selected', 'selected');
    }
    if(check == '否'){
        document.getElementById('check').options[1].setAttribute('selected', 'selected');
    }else{
        document.getElementById('check').options[0].setAttribute('selected', 'selected');
    }
    if(update == '否'){
        document.getElementById('update').options[1].setAttribute('selected', 'selected');
    }else{
        document.getElementById('update').options[0].setAttribute('selected', 'selected');
    }
}
function hide(){
    document.getElementById('cover').style.display="none";
}
function add(){
    document.getElementById('cover_box_add').style.display="";
    document.getElementById('cover').style.display="";
    document.getElementById('cover_box_update').style.display="none";
}