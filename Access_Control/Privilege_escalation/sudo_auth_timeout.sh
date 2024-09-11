grep -roP "timestamp_timeout=\K[0-9]*" /etc/sudoers*
#timeout<=15
sudo -V | grep "Authentication timestamp timeout:"
#timeout == 15