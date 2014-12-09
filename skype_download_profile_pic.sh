#!/bin/bash
user="$1"
if [ "$user" == "" ]; then
	echo "Username?"
	read user
fi
wget "api.skype.com/users/$user/profile/avatar" -O "$user.jpg"
if [ "$?" != "0" ]; then
	echo "Unable to download profile image. Check above for errors"
	exit
else
	echo "Profile pic of $user downloaded to $user.jpg"
fi
exit

