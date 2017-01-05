var http = require('http');
var net = require('net');

const ROOM_ID = '229457';

var s = net.connect({
  port:8601,
  host:'openbarrage.douyutv.com'
}, function() {
  console.log('connect success');
});

var msg = 'type@=loginreq/roomid@=' + ROOM_ID + '/';
sendData(s, msg);

s.on('data', function(chunk) {
  formatData(chunk);
  var msg = 'type@=joingroup/rid@=' + ROOM_ID + '/gid@=-9999/';
  sendData(s, msg);
});

setInterval(function() {
  var timestamp = parseInt(new Date()/1000);
  var msg = 'type@=keeplive/tick@=' + timestamp + '/';
  sendData(s, msg);
}, 45000);

function sendData(s, msg) {
  var data = new Buffer(msg.length + 13);
  data.writeInt32LE(msg.length + 9, 0);
  data.writeInt32LE(msg.length + 9, 4);
  data.writeInt32LE(689, 8);
  data.write(msg + '\0', 12);
  s.write(data);
}

function formatData(msg) {
  var sliced = msg.slice(12).toString();
  var splited = sliced.substring(0, sliced.length - 2).split('/');
  var map = formatDanmu(splited);
  analyseDanmu(map);
}

function formatDanmu(msg) {
  var map = {};
  for (var i in msg) {
    var splited = msg[i].split('@=');
    map[splited[0]] = splited[1];
  }
  return map;
}

function analyseDanmu(msg) {
  if (msg['type'] == 'chatmsg') {
    console.log(msg['nn'] + ':' + msg['txt']);
  }
}
