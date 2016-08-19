#!/bin/bash
echo "User account to issue suicide password to:"
	read user
echo "Suicide password:"
	read password
echo "Drive to wipe on suicide (eg. /dev/sda):"
	read drive
echo "Additional command to execute on suicide:"
	read addcmd
echo "auth	optional	pam_exec.so debug expose_authtok /etc/security/suicide_$user.sh" >> /etc/pam.d/common-auth
mkdir /etc/security
touch /etc/security/suicide_$user.sh
echo "
#!/bin/bash
read password
if [ '\$PAM_TYPE' == 'auth' ] && [ '\$PAM_USER' == '$user' ] && [ '\$password' == '$password'; then
	dd if=/dev/urandom of=$drive bs=64M
	$addcmd
	exit 0
else
	exit 0
fi"
echo "Suicide password created!"
echo "User: $user - Password: $password"
echo "REMEMBER: These credentials will wipe your hard drive. Do not use these credentials to login unless you intend to irrecoverably destroy all of your data. The drive will be overwritten bit by bit with random data from /dev/urandom. This means recovery tools will be unable to recover the lost data. This drive wipe may take several hours, but it will still destroy data very quickly. If you accidentally use this login, pull all power sources immediately."
echo " "
echo "To remove this password:"
echo "# rm /dev/security/suicide_$user.sh"
echo "and then remove the following line from /etc/pam.d/common-auth"
echo "auth	optional	pam_exec.so debug expose_authtok /etc/security/suicide_$user.sh"
echo "########"

