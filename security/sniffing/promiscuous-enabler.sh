#!/bin/bash
user=$(whoami)
if [ "$user" != "root" ]; then
	echo "This script must be run as root (sudo). Currently running as $user. Exiting."
	exit
fi
echo "Add/Remove Promiscuous? (+/-)"
	read whatdo
echo "Interface to affect: (wlan0, etho0, etc.)"
	read interface
if [ "$whatdo" == "+" ]; then
	ifconfig "$interface" promisc
	if [ "$?" != "0" ]; then
		echo "Failed."
	else
		echo "Succeeded."
	fi
elif [ "$whatdo" == "-" ]; then
	ifconfig "$interface" -promisc
	if [ "$?" != "0" ]; then
		echo "Failed."
	else
		echo "Succeeded."
	fi
else
	echo "Invalid option. (must be '+' or '-')"
fi
