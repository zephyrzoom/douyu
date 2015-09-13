#python3
import socket
import time
import threading
import json


g_cid= 15111
g_ip= 'livecmt.bilibili.com'
g_port= 88
g_exit= False
g_res_00_02_msginfo= ['num0','num1','num2','num3','num4','num5','num6','num7','num8']
g_res_00_02_userinfo= ['num0','username','num2']
g_res_00_02= ['msginfo','msg','userinfo']


def sendmsg(s,code,msg):
    #code(2byte)  length(2byte)
    data_length= len(msg)+4
    sd= code[0:2]+int.to_bytes(data_length,2,'big')+msg

    sent=0
    while sent<len(sd):
        tn= s.send(sd[sent:])
        sent= sent + tn

def recvmsg(s):
    #type 2byte
    bdata_type= s.recv(2)
    if not bdata_type:
        return None,None
    if bdata_type==b'\x00\x02':
        #length 2byte
        data_length= int.from_bytes(s.recv(2),'big')-4
        #msg
        if data_length<0:
            print('badlength',data_length)
            return bdata_type, b'undifined'
        total_data=[]
        while data_length>0:
            msg= s.recv(data_length)
            data_length= data_length - len(msg)
            total_data.append(msg)
        ret= b''.join(total_data)
    elif bdata_type==b'\x00\x01':
        ret= s.recv(4)
    else:
        print('unknow package type:', bdata_type)
        return bdata_type, b'undifined'
    return bdata_type, ret

def unpackage(data):
    try:
        #ret= json.loads(data.replace(b"\\\'",b"\'").replace(b'\\t',b'\t').decode('utf8'))
        ret= eval(data)
        return ret
    except:
        print('unable decode json.', data)

def get_danmu():
    print('==========danmu')
    global g_cid
    global g_exit
    global g_res_00_02
    global g_res_00_02_userinfo


    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((g_ip,int(g_port)))
    #login
    sendmsg(s, b'\x01\x01', int.to_bytes(g_cid,4,'big')+b'\x00\x00\x00\x00')
    if recvmsg(s)[0] == b'\x00\x01':
        print('success!')

    def keepalive():
        global g_exit
        print('==========keepalive')
        while not g_exit:
            sendmsg(s, b'\x01\x02', b'')
            time.sleep(30)
        s.close()
    threading.Thread(target=keepalive).start()

    while True:
        msgtype,bmsg= recvmsg(s)

        if msgtype==b'\x00\x01': 
            print('***', 'live-count: ', int.from_bytes(bmsg,'big'),'***')
        elif msgtype==b'\x00\x02': #msg
            msg= unpackage(bmsg)
            msg_dict= dict(zip(g_res_00_02, msg))
            msg_userinfo_dict= dict(zip(g_res_00_02_userinfo, msg_dict['userinfo']))
            nick= msg_userinfo_dict['username']
            content= msg_dict['msg']
            print(nick, ': ', content)
        elif msgtype==None:
            print('*** connection break ***')
            g_exit= True
            break
        else:
            print(bmsg)
            

get_danmu()
