if [[ $1 == "no" ]] ;
then
dpkg-query -s samba &>/dev/null && echo "samba is installed"
else
systemctl is-enabled smbd.service 2>/dev/null | grep 'enabled'
systemctl is-active smbd.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
