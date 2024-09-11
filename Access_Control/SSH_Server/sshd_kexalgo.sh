sshd -T | grep -Pi -- 'kexalgorithms\h+([^#\n\r]+,)?(diffie-hellman-group1- sha1|diffie-hellman-group14-sha1|diffie-hellman-group-exchange-sha1)\b'
#nothing should be returned
#these should not be there
# diffie-hellman-group1-sha1
# diffie-hellman-group14-sha1
# diffie-hellman-group-exchange-sha1