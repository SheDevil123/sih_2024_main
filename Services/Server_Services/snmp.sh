if [[ $1 == "no" ]] ;
then
dpkg-query -s snmpd &>/dev/null && echo "snmpd is installed"
else
systemctl is-enabled snmpd.service 2>/dev/null | grep 'enabled'
systemctl is-enabled snmpd.service 2>/dev/null | grep 'enabled'
fi

#nothing should be returned
