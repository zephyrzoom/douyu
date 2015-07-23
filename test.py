import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('119.90.49.107', 8034))

s.sendall(b'type@=loginreq/username@=auto_qZ1JCRPZC6/password@=596a96cc7bf9108cd896f33c44aedc8a/roompass@=/roomid@=265352/devid@=5DCE2FFCE0E61AB11F77D935D10E6E0B/rt@=1437381860/vk@=f78f45ff359eceeafbf1a0d2e2b9874b/ver@=20150714/')
data = s.recv(1024)
s.close()
print('Received', repr(data))

#  public static byte[] loginReq(string username,string password,string roomid,string uuid)
#        {
#            long time=Scholar.Framework.Utils.Util.UNIX_TIMESTAMP();
#            string salt="7oE9nPEG9xXV69phU31FYCLUagKeYtsF";
#            string vk=Scholar.Framework.Utils.Util.Md5(string.Format("{0}{1}{2}",time,salt,uuid));
#            string p = string.Format("type@=loginreq/username@={0}/password@={1}/roomid@=
#                                           {2}/ct@=2/devid@={3}/ver@={4}/rt@={5}/vk@={6}/",
#                username, password, roomid, uuid, 20150515,time,vk);
#            byte[] bin = Encoding.UTF8.GetBytes(p);
#            ByteBuffer buf = new ByteBuffer();
#            buf.Put("dc000000 dc000000 b1020000 ");
#            buf.Put(bin);
#            buf.Put(0);
#            return buf.ToByteArray();
#        }

#urlgreq is [type@=loginreq/username@=auto_qZ1JCRPZC6/
# password@=596a96cc7bf9108cd896f33c44aedc8a/roompass@=/
# roomid@=265352/devid@=5DCE2FFCE0E61AB11F77D935D10E6E0B/
# rt@=1437381860/vk@=f78f45ff359eceeafbf1a0d2e2b9874b/ver@=20150714/]