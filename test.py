import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('119.90.49.103', 8011))

#s.sendall(b'type@=loginreq/username@=auto_qZ1JCRPZC6/password@=596a96cc7bf9108cd896f33c44aedc8a/roompass@=/roomid@=265352/devid@=5DCE2FFCE0E61AB11F77D935D10E6E0B/rt@=1437381860/vk@=f78f45ff359eceeafbf1a0d2e2b9874b/ver@=20150714/')
time.sleep(4)
s.sendall(b'e1000000e1000000b102000074797065403d6c6f67696e7265712f757365726e616d65403d6175746f5f715a314a4352505a43362f70617373776f7264403d35393661393663633762663931303863643839366633336334346165646338612f726f6f6d70617373403d2f726f6f6d6964403d3232393435372f6465766964403d35444345324646434530453631414231314637374439333544313045364530422f7274403d313433373635333132332f766b403d33653732353038666430373562643464666133666535373233336666613337322f766572403d32303135303732312f00')
time.sleep(1)
s.sendall(b'3100000031000000b102000074797065403d6f6e6c696e655f676966745f696e666f5f7265712f756964403d323233363431372f00')
s.sendall(b'4200000042000000b102000074797065403d6d656d626572696e666f7265712f6c696e6b403d687474703a405340537777772e646f75797574762e636f6d40537a65656b2f00')
while True:
    time.sleep(1)
    s.sendall(b'5b0000005b000000b102000074797065403d6b6565706c6976652f7469636b403d313433373635333132332f766277403d302f63646e403d302f6b403d35393664653332353533373164636133653338653639306538643839356135312f00')
    time.sleep(2)
    data = s.recv(5)
    print('Received', repr(data))

s.close()


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