if [[ $1 == "no" ]] ;
then
dpkg-query -s isc-dhcp-server &>/dev/null && echo "isc-dhcp-server is installed"
else
systemctl is-enabled isc-dhcp-server.service isc-dhcp-server6.service 2>/dev/null | grep 'enabled'
systemctl is-active isc-dhcp-server.service isc-dhcp-server6.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
