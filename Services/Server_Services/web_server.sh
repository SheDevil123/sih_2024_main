if [[ $1 == "no" ]] ;
then
dpkg-query -s apache2 &>/dev/null && echo "apache2 is installed"
dpkg-query -s nginx &>/dev/null && echo "nginx is installed"
else
systemctl is-enabled apache2.socket apache2.service nginx.service 2>/dev/null | grep 'enabled'
systemctl is-active apache2.socket apache2.service nginx.service 2>/dev/null | grep '^active'
fi

#nothing should be returned
