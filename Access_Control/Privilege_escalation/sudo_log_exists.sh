grep -rPsi "^\h*Defaults\h+([^#]+,\h*)?logfile\h*=\h*(\"|\')?\H+(\"|\')?(,\h*\H+\h*)*\h* (#.*)?$" /etc/sudoers*
#Defaults logfile="/var/log/sudo.log"