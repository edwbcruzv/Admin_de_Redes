#!/bin/bash

sudo tunctl -u cruz

sudo ifconfig tap0 192.168.1.2/24 up

ifconfig

sudo route -v

sudo route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1 dev tap0

sudo route -v