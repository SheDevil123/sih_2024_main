if [[ $1 == "no" ]] ;
then
dpkg-query -s cups &>/dev/null && echo "cups is installed"
else
systemctl is-enabled cups.socket cups.service 2>/dev/null | grep 'enabled'
systemctl is-active cups.socket cups.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
