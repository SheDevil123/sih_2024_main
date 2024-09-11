sshd -T | grep -Pi -- '^ciphers\h+\"?([^#\n\r]+,)?((3des|blowfish|cast128|aes(128|192|256))- cbc|arcfour(128|256)?|rijndael-cbc@lysator\.liu\.se|chacha20- poly1305@openssh\.com)\b'

#none of these lines to be returned
# 3des-cbc
# aes128-cbc
# aes192-cbc
# aes256-cbc