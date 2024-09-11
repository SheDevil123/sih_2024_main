#grep -Pi -- '^\h*PASS_WARN_AGE\h+\d+\b' /etc/login.defs
# PASS_WARN_AGE >=7
awk -F: '($2~/^\$.+\$/) {if($6 < 7)print "User: " $1 " PASS_WARN_AGE: " $6}' /etc/shadow
#nothing should be returned
