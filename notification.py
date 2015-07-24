__author__ = 'zeek'
import notify2
import platform

sysinfo = platform.system()

print(sysinfo)
notify2.init("douyu")

header = "D.:"
content = "hello"
n = notify2.Notification(header,
                         sysinfo
                         )
n.show()
