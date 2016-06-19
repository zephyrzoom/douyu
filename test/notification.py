__author__ = 'zeek'
import notify2
import platform
import os

sysinfo = platform.system()

print(sysinfo)
notify2.init("douyu")

header = "D.:"
content = "hello"
n = notify2.Notification(header,
                         sysinfo
                         )
#n.show()
print('notify-send {}'.format(': '.join(['a', 'b'])))
os.system('notify-send {}'.format(': '.join(['a', 'b'])))
