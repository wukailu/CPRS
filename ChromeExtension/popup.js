function getRecommend(username){
  if(!connected){
    $("#recommend").text("connect Failed!");
    return;
  }
  connection.send(username);
}

function refresh(e){
  getRecommend($("#user_name").val());
}

$( function () {
  $("#refresh").click(refresh);
  connection = new WebSocket('ws://127.0.0.1:2340');
  connected = false;
  connection.onopen = function () {
    console.log("Connected!");
    connected = true; 
  };
  connection.onmessage = function(e){
    $("#recommend").text(e.data);  
  };
  window.onbeforeunload = function(){
    connection.close();
  }
});

