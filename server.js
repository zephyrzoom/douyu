#!/usr/bin/env node
var net = require('net');
var PORT= 8602;
var HOST='danmu.douyu.tv'

var server = net.createServer(function(c) { 
  console.log('PS4已连接');
connectdouyu(c);


c.on('end', function() {
    console.log('PS4断开');
  });
c.on('data',function(data){
//模拟irc.twitch.tv服务器
var match = /^(\w+)\s+(.*)/.exec(data);
		if (!match) {
			return;
		}
var conn;
var command = match[1].toUpperCase(),
			rest = match[2];
//console.log("Command:"+command+"   Rest:"+rest);
switch (command) {
case "PASS":
c.write(":tmi.twitch.tv 001 jocover :Welcome, GLHF!\r\n","ascii");
c.write(":tmi.twitch.tv 002 jocover :Your host is tmi.twitch.tv\r\n","ascii");
c.write(":tmi.twitch.tv 003 jocover :This server is rather new\r\n","ascii");
c.write(":tmi.twitch.tv 004 jocover :-\r\n","ascii");
c.write(":tmi.twitch.tv 375 jocover :-\r\n","ascii");
c.write(":tmi.twitch.tv 372 jocover :You are in a maze of twisty passages, all alike.\r\n","ascii");
c.write(":tmi.twitch.tv 376 jocover :>\r\n","ascii");
break;

case "JOIN":
c.write(":jocover!jocover@jocover.tmi.twitch.tv JOIN #jocover\r\n","ascii");
c.write(":jocover.tmi.twitch.tv 353 jocover = #jocover :jocover\r\n","ascii");

break;

default:
console.log("Unknow command :"+command+' Rest:'+rest);
break;
}

});
});


function connectdouyu (msg){
var client = net.connect(PORT,HOST,
    function() { //'connect' listener
  console.log('连接斗鱼弹幕服务器');
  client.removeAllListeners('data');
client.setKeepAlive('true',1000);
sleep(4);
  client.write('5a0000005a000000b102000074797065403d6c6f67696e7265712f757365726e616d65403d6175746f5f615a464c4a687255696c2f70617373776f7264403d313233343536373839303132333435362f726f6f6d6964403d353830322f00','hex');
sleep(1);
  client.write('2a0000002a000000b102000074797065403d6a6f696e67726f75702f726964403d353830322f676964403d302f00','hex');

client.on('connect',function(){});

setInterval(function(){
//斗鱼弹幕心跳包，5000ms循环发送一次
client.write('2100000021000000b202000074797065403d6b6565706c6976652f7469636b403d34382f00','hex');
},5000);

client.on('error',function(err){
console.log('error:'+err.toString("ascii"));
});


client.on('data', function(data) {
        //console.log(data.toString());获取弹幕信息
        var match = data.toString();
        if(match.indexOf("chatmessage")>1){
        var name = match.substring(match.indexOf("snick@=") + 7, match.indexOf("/cd@"));
        var message = match.substring(match.indexOf("content@") + 9, match.indexOf("/snick@"));
        try {
       	msg.write(":" + name + "!" + name + "@" + name + ".tmi.twitch.tv PRIVMSG #jocover :" + message + "\r\n");
    	} catch(ex) {
      		console.log(ex);
    	}
       
	 }

});
client.on('end', function() {
  console.log('斗鱼弹幕服务器断开\n');
});

});
}




function sleep(milliSeconds) { 
    var startTime = new Date().getTime(); 
    while (new Date().getTime() < startTime + milliSeconds);
 };



server.listen(6667, function() { //'listening' listener
  console.log('系统运行');
});
