if [[ $1 == "no" ]] ;
then
dpkg-query -s dnsmasq &>/dev/null && echo "dnsmasq is installed"
else
systemctl is-enabled dnsmasq.service 2>/dev/null | grep 'enabled'
systemctl is-active dnsmasq.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
