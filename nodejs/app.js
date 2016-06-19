var http = require('http');
var net = require('net');

var s = net.connect({
  port:8601,
  host:'openbarrage.douyutv.com'
}, function() {
  console.log('connect success');
});

var msg = 'type@=loginreq/roomid@=229457/';
sendData(s, msg);

s.on('data', function(chunk) {
  formatData(chunk);
  var msg = 'type@=joingroup/rid@=229457/gid@=-9999/';
  sendData(s, msg);
});

setInterval(function() {
  var msg = 'type@=keeplive/tick@=1439802131/';
  sendData(s, msg);
}, 45000);

function sendData(s, msg) {
  var data = new Buffer(4 + 4 + 4 + msg.length + 1);
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
