grep "^\s*linux" /boot/grub/grub.cfg | grep -v "apparmor=1"

 grep "^\s*linux" /boot/grub/grub.cfg | grep -v "security=apparmor"
