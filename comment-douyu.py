import socket
import time
import random
import threading
import re
import json
import sys
import os
import platform
import notify2
from urllib import request

g_rid= b'265352'
g_username= b'visitor42'
g_ip= b'danmu.douyutv.com'
g_port= 8601
g_gid= b'0'
g_exit= False
sysinfo = platform.system()

def notify(title, message):
    if sysinfo == 'Linux':
        os.system('notify-send {}'.format(': '.join([title, message])))
#        notify2.init('douyu')
#        notify2.Notification(title, message).show()
    else:
        t = '-title {!r}'.format(title)
        m = '-message {!r}'.format(message)
        os.system('terminal-notifier {}'.format(' '.join([m, t])))


def is_exit():
    global g_exit
    return g_exit

def cast_wetght(g):
    g= int(g)
    if g>1e6:
        return str(round(g/1e6,2))+'t'
    elif g>1e3:
        return str(round(g/1e3,2))+'kg'
    else:
        return str(g)+'g'

def sendmsg(s,msg,code=689):
    data_length= len(msg)+8
    s.send(int.to_bytes(data_length,4,'little'))
    s.send(int.to_bytes(data_length,4,'little'))
    s.send(int.to_bytes(code,4,'little'))
    sent=0
    while sent<len(msg):
        tn= s.send(msg[sent:])
        sent= sent + tn

def recvmsg(s):
    bdata_length= s.recv(12)
    data_length= int.from_bytes(bdata_length[:4],'little')-8
    if data_length<=0:
        print('badlength',bdata_length)
        return None
    total_data=[]
    while True:
        msg= s.recv(data_length)
        if not msg: break
        data_length= data_length - len(msg)
        total_data.append(msg)
    ret= b''.join(total_data)
    return ret

def unpackage(data):
    ret={}
    lines= data.split(b'/')
    lines.pop() # pop b''
    for line in lines:
        kv= line.split(b'@=')
        if len(kv)==2:
            ret[kv[0]]= kv[1].replace(b'@S',b'/').replace(b'@A',b'@')
        else:
            ret[len(ret)]= kv[0].replace(b'@S',b'/').replace(b'@A',b'@')

    return ret

def unpackage_list(l):
    ret=[]
    lines= l.split(b'@S')
    for line in lines:
        line= line.replace(b'@AA',b'')
        mp= line.split(b'@AS')
        tb={}
        for kv in mp:
            try:
                k,v= kv.split(b'=')
                tb[k]=v
            except:
                pass
        ret.append(tb)
    return ret

def get_longinres(s_ip=b'117.79.132.20', s_port=8001, rid=b'265352'):
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((s_ip, int(s_port)))

    sendmsg(s,b'type@=loginreq/username@=/password@=/roomid@='+rid+b'/\x00')

    print('==========longinres')
    longinres= unpackage(recvmsg(s))

    #print('==========msgrepeaterlist')
    msgrepeaterlist= unpackage(recvmsg(s))
    lst= unpackage(msgrepeaterlist[b'list'])
    tb= unpackage(random.choice(tuple(lst.values())))

    #print('==========setmsggroup')
    setmsggroup= unpackage(recvmsg(s))
    
    ret= {'rid':rid,
          'username': longinres[b'username'],
          'ip': tb[b'ip'],
          'port': tb[b'port'],
          'gid': setmsggroup[b'gid']
         }

    def keepalive_send():
        while not is_exit():
            sendmsg(s,b'type@=keeplive/tick@='+str(random.randint(1,99)).encode('ascii')+b'/\x00')
            time.sleep(45)
        s.close()
    threading.Thread(target=keepalive_send).start()
    def keepalive_recv():
        while not is_exit():
            bmsg= recvmsg(s)
            print('*** usr alive:',unpackage(bmsg),'***')
        s.close()
    threading.Thread(target=keepalive_recv).start()
    return ret

def get_danmu(rid=b'5275', ip=b'danmu.douyutv.com', port=8001, username=b'visitor42', gid=b'0'):
    "args needs bytes not str"
    print('==========danmu')

    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,int(port)))
    sendmsg(s,b'type@=loginreq/username@='+username+b'/password@=1234567890123456/roomid@='+rid+b'/\x00')
    loginres= unpackage(recvmsg(s))
    sendmsg(s,b'type@=joingroup/rid@='+rid+b'/gid@='+gid+b'/\x00')

    def keepalive():
        while not is_exit():
            sendmsg(s,b'type@=keeplive/tick@='+str(random.randint(1,99)).encode('ascii')+b'/\x00')
            time.sleep(45)
        s.close()
    threading.Thread(target=keepalive).start()

    while True:
        bmsg= recvmsg(s)
        if not bmsg:
            print('*** connection break ***')
            global g_exit
            g_exit= True
            break

        msg= unpackage(bmsg)
        msgtype= msg.get(b'type',b'undefined')

        if msgtype==b'chatmessage':
                nick= msg[b'snick'].decode('utf8')
                content= msg.get(b'content',b'undefined').decode('utf8')
                print(nick, ': ', content)
                notify(nick, content)
        elif msgtype==b'donateres':
            sui= unpackage(msg.get(b'sui',b'nick@=undifined//00'))
            nick= sui[b'nick'].decode('utf8')
            print('***', nick, '送给主播', int(msg[b'ms']),\
                  '个鱼丸 (', cast_wetght(msg[b'dst_weight']), ') ***')
            notify(nick, '送给主播' + str(int(msg[b'ms'])) + '个鱼丸')
        elif msgtype==b'keeplive':
            print('*** dm alive:',msg,'***')
        elif msgtype in (b'userenter'):
            pass
        else:
            print(msg)

###########from common.py
def match1(text, *patterns):
    """Scans through a string for substrings matched some patterns (first-subgroups only).

    Args:
        text: A string to be scanned.
        patterns: Arbitrary number of regex patterns.

    Returns:
        When only one pattern is given, returns a string (None if no match found).
        When more than one pattern are given, returns a list of strings ([] if no match found).
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret

def get_content(url, headers={}, decoded=True, cookies_txt=''):
    """Gets the content of a URL via sending a HTTP GET request.

    Args:
        url: A URL.
        headers: Request headers used by the client.
        decoded: Whether decode the response body using UTF-8 or the charset specified in Content-Type.

    Returns:
        The content as a string.
    """

    req = request.Request(url, headers=headers)
    if cookies_txt:
        cookies_txt.add_cookie_header(req)
        req.headers.update(req.unredirected_hdrs)
    response = request.urlopen(req)
    data = response.read()

    # Handle HTTP compression for gzip and deflate (zlib)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = ungzip(data)
    elif content_encoding == 'deflate':
        data = undeflate(data)

    # Decode the response body
    if decoded:
        charset = match1(response.getheader('Content-Type'), r'charset=([\w-]+)')
        if charset is not None:
            data = data.decode(charset)
        else:
            data = data.decode('utf-8')

    return data
###########from util/strings.py
try:
  # py 3.4
  from html import unescape as unescape_html
except ImportError:
  import re
  from html.entities import entitydefs

  def unescape_html(string):
    '''HTML entity decode'''
    string = re.sub(r'&#[^;]+;', _sharp2uni, string)
    string = re.sub(r'&[^;]+;', lambda m: entitydefs[m.group(0)[1:-1]], string)
    return string

  def _sharp2uni(m):
    '''&#...; ==> unicode'''
    s = m.group(0)[2:].rstrip(';；')
    if s.startswith('x'):
      return chr(int('0'+s, 16))
    else:
      return chr(int(s))
##########

def get_room_info(url):
    print('==========room')
    html = get_content(url)
    room_id_patt = r'"room_id":(\d{1,99}),'
    title_patt = r'<div class="headline clearfix">\s*<h1>([^<]{1,9999})</h1>'
    title_patt_backup = r'<title>([^<]{1,9999})</title>'
    
    roomid = match1(html,room_id_patt)
    title = match1(html,title_patt) or match1(html,title_patt_backup)
    title = unescape_html(title)

    conf = get_content("http://www.douyutv.com/api/client/room/"+roomid)
    metadata = json.loads(conf)
    servers= metadata['data']['servers']
    dest_server= servers[0]
    return {'s_ip': dest_server['ip'],
            's_port': dest_server['port'],
            'rid': metadata['data']['room_id'].encode()
           }
    print(metadata)

def main(url='http://www.douyutv.com/xtd'):
    login_user_info= get_room_info(url)
    print('login_user_info:', login_user_info)

    login_room_info= get_longinres(**login_user_info)
    print('login_room_info', login_room_info)

    get_danmu(**login_room_info)

if __name__=='__main__':
    url= sys.argv[1] if len(sys.argv)>1 else 'http://www.douyutv.com/zeek'
    main(url)
