stat -Lc 'Access: (%a/%A) Owner: (%U) Group: (%G)' /etc/cron.allow

# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# or 'stat: cannot statx '/etc/cron.allow': No such file or directory'
# if 'no such file' output then execute the last line and verify output is 
# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# or no output is returned

[ -e "/etc/cron.deny" ] && stat -Lc 'Access: (%a/%A) Owner: (%U) Group: (%G)' /etc/cron.deny
