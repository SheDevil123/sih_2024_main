if [[ $1 == "no" ]] ;
then
dpkg-query -s tftpd-hpa &>/dev/null && echo "tftpd-hpa is installed"
else
systemctl is-enabled tftpd-hpa.service 2>/dev/null | grep 'enabled'
systemctl is-active tftpd-hpa.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
