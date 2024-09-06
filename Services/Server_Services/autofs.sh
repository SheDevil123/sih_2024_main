if [[ $1 == "no" ]] ;
then
	dpkg-query -s autofs &>/dev/null && echo "autofs is installed"
else
	systemctl is-enabled autofs.service 2>/dev/null | grep 'enabled'
	systemctl is-active autofs.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
