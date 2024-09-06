stat -Lc 'Access: (%a/%A) Owner: (%U) Group: (%G)' /etc/at.allow
# Access: (640/-rw-r-----) Owner: (root) Group: (daemon)
# -OR-
# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# Access is 0640 or less
# if output is 'stat: cannot statx '/etc/at.allow': No such file or directory'
# run below line and verify output is as follows
[ -e "/etc/at.deny" ] && stat -Lc 'Access: (%a/%A) Owner: (%U) Group: (%G)' /etc/at.deny
# Access: (640/-rw-r-----) Owner: (root) Group: (daemon)
# -OR-
# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# -OR-
# Nothing is returned
# access is 0640 or less
