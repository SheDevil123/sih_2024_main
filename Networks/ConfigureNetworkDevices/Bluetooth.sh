dpkg-query -s bluez &>/dev/null && echo "bluez is installed"
systemctl is-enabled bluetooth.service 2>/dev/null | grep 'enabled'
systemctl is-active bluetooth.service 2>/dev/null | grep '^active'
#Nothing_should_be_returned
