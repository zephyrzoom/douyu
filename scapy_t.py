__author__ = 'zeek'
from scapy.all import *

sniff(iface="wifi0", prn=lambda x: x.summary())
