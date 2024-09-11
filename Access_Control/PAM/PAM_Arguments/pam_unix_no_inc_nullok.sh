grep -PH -- '^\h*^\h*[^#\n\r]+\h+pam_unix\.so\b' /etc/pam.d/common- {password,auth,account,session,session-noninteractive} | grep -Pv -- '\bnullok\b'

# /etc/pam.d/common-password:password [success=1 default=ignore]
# pam_unix.so obscure use_authtok try_first_pass yescrypt
# /etc/pam.d/common-auth:auth [success=2 default=ignore] pam_unix.so
# try_first_pass
# /etc/pam.d/common-account:account [success=1 new_authtok_reqd=done
# default=ignore] pam_unix.so
# /etc/pam.d/common-session:session required pam_unix.so
# /etc/pam.d/common-session-noninteractive:session required pam_unix.so