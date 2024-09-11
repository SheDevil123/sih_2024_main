grep -PH -- '^\h*password\h+([^#\n\r]+)\h+pam_unix\.so\h+([^#\n\r]+\h+)?use_authtok\b' /etc/pam.d/common-password

# /etc/pam.d/common-password:password [success=1 default=ignore]
# pam_unix.so obscure use_authtok try_first_pass yescrypt