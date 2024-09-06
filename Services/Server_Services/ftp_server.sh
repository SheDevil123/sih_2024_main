if [[ $1 == "no" ]] ;
then
dpkg-query -s vsftpd &>/dev/null && echo "vsftpd is installed"
else
systemctl is-enabled vsftpd.service 2>/dev/null | grep 'enabled'
systemctl is-active vsftpd.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
