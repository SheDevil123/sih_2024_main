if [[ $1 == "no" ]] ;
then
dpkg-query -s slapd &>/dev/null && echo "slapd is installed"
else
systemctl is-enabled slapd.service 2>/dev/null | grep 'enabled'
systemctl is-active slapd.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
