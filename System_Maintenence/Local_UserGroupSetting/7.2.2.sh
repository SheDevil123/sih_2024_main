awk -F: '($2 == "" ) { print $1 " does not have a password "}' /etc/shadow
#nothing should be returned (root)
