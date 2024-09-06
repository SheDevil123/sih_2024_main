if [[ $1 == "no" ]] ;
then
	dpkg-query -s avahi-daemon &>/dev/null && echo "avahi-daemon is installed"
else
	systemctl is-enabled avahi-daemon.socket avahi-daemon.service 2>/dev/null |grep 'enabled'
	systemctl is-active avahi-daemon.socket avahi-daemon.service 2>/dev/null |grep '^active'
fi

#nothing should be returned
