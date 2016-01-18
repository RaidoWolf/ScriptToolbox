#!/bin/bash
whoami="$(whoami)"
if [ "$whoami" == "root" ]; then
	apt-get install libdvdread4
	/usr/share/doc/libdvdread4/install-css.sh
else
	echo "This script must be run as root! Currently running as $whoami."
	exit
fi
