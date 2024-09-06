if [[ $1 == "no" ]] ;
then
dpkg-query -s ypserv &>/dev/null && echo "ypserv is installed"
else
systemctl is-enabled ypserv.service 2>/dev/null | grep 'enabled'
systemctl is-active ypserv.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
