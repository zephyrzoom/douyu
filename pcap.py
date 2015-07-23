__author__ = 'zeek'
import pure_pcapy
from impacket.ImpactDecoder import *

# list all the network devices
pure_pcapy.findalldevs()

max_bytes = 1024
promiscuous = False
read_timeout = 100  # in milliseconds
pc = pure_pcapy.open_live("chrome", max_bytes,
                          promiscuous, read_timeout)

pc.setfilter('tcp')


# callback for received packets
def recv_pkts(hdr, data):
    packet = EthDecoder().decode(data)
    print(packet)


packet_limit = -1  # infinite
pc.loop(packet_limit, recv_pkts)  # capture packets
