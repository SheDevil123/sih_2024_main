if [[ $1 == "no" ]] ;
then
dpkg-query -s rpcbind &>/dev/null && echo "rpcbind is installed"
else
systemctl is-enabled rpcbind.socket rpcbind.service 2>/dev/null | grep 'enabled'
systemctl is-active rpcbind.socket rpcbind.service 2>/dev/null | grep '^active'
fi

#nothing should be returned 
