if [[ $1 == "no" ]] ;
then
dpkg-query -s rsync &>/dev/null && echo "rsync is installed"
else
systemctl is-enabled rsync.service 2>/dev/null | grep 'enabled'
systemctl is-active rsync.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
