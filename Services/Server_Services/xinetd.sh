if [[ $1 == "no" ]] ;
then
dpkg-query -s xinetd &>/dev/null && echo "xinetd is installed"
else
systemctl is-enabled xinetd.service 2>/dev/null | grep 'enabled'
systemctl is-active xinetd.service 2>/dev/null | grep '^active'
fi
#nothing should be returned
