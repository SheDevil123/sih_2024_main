if [[ $1 == "no" ]] ;
then
dpkg-query -s bind9 &>/dev/null && echo "bind9 is installed"
else
systemctl is-enabled bind9.service 2>/dev/null | grep 'enabled'
systemctl is-active bind9.service 2>/dev/null | grep '^active'
fi
#nothing should be returned
