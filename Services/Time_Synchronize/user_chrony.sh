ps -ef | awk '(/[c]hronyd/ && $1!="_chrony") { print $1 }'
#nothing should be returned
