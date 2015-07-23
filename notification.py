__author__ = 'zeek'
import notify2

notify2.init("douyu")

header = "D.:"
content = "hello"
n = notify2.Notification(header,
                         content,
                         )
n.show()
