if [[ $1 == "no" ]] ;
then
dpkg-query -s squid &>/dev/null && echo "squid is installed"
else
systemctl is-enabled squid.service 2>/dev/null | grep 'enabled'
systemctl is-active squid.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
