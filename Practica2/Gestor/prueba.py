from pysnmp.hlapi import *
import rrdtool

last_update = rrdtool.lastupdate("miUDP.rrd")
print(last_update)