[ -e "/etc/security/opasswd" ] && stat -Lc '%n Access: (%a/%A) Uid: (%u/ %U) Gid: ( %g/ %G)' /etc/security/opasswd

[ -e "/etc/security/opasswd.old" ] && stat -Lc '%n Access: (%a/%A) Uid:( %u/ %U) Gid: ( %g/ %G)' /etc/security/opasswd.old

# OUTPUT IS /etc/security/opasswd Access: (0600/-rw-------) Uid: (0/ root) Gid: ( 0/ root)

