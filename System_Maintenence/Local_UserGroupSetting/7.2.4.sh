awk -F: '($1=="shadow") {print $NF}' /etc/group
awk -F: '($4 == '"$(getent group shadow | awk -F: '{print $3}' | xargs)"')
{print " - user: \"" $1 "\" primary group is the shadow group"}' /etc/passwd

# no result should be returened
