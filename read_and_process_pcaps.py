import csv
import os
from scapy.all import *

packets = rdpcap("./mega104-17-12-18_FILTERED.pcapng")

# We are interested in inter-arrival time of packets (and maybe their size?), split it to direction FROM MASTER and TO MASTER
packets_len = len(packets)

f = open('packets_to_m.csv', 'w')
g = open('packets_from_m.csv', 'w')

to_masterwriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
from_masterwriter = csv.writer(g, delimiter=',', quoting=csv.QUOTE_NONE)

for index, pkt in enumerate(packets):
    p_size = len(pkt)

    if (index+1 < packets_len and index - 1 >= 0):
        p_atime = pkt.time-packets[index-1].time
    else:
        p_atime = 0.0

    if TCP in pkt:
        tcp_dport = pkt[TCP].dport
    if(tcp_dport == 2404):
        #TO_MASTER
        to_masterwriter.writerow([p_atime, p_size])
        
    else:
        #FROM_MASTER
        from_masterwriter.writerow([p_atime, p_size])

f.close()
g.close()