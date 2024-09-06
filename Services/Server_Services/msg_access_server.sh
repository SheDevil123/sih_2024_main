if [[ $1 == "no" ]] ;
then
dpkg-query -s dovecot-imapd &>/dev/null && echo "dovecot-imapd is installed"
else
dpkg-query -s dovecot-pop3d &>/dev/null && echo "dovecot-pop3d is installed"
systemctl is-enabled dovecot.socket dovecot.service 2>/dev/null | grep 'enabled'
fi

#nothing should be returned
