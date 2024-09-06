if [[ $1 == "no" ]] ;
then
systemctl is-enabled dovecot.socket dovecot.service 2>/dev/null | grep 'enabled'
else
systemctl is-enabled nfs-server.service 2>/dev/null | grep 'enabled'
systemctl is-active nfs-server.service 2>/dev/null | grep '^active'
fi


#nothing should be returned
