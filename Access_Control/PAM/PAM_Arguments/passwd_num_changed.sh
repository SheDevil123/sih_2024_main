grep -Psi -- '^\h*difok\h*=\h*([2-9]|[1-9][0-9]+)\b' /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf

#eg output
#/etc/security/pwquality.conf.d/50-pwdifok.conf:difok >=2

grep -Psi -- '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\ r]+\h+)?difok\h*=\h*([0-1])\b' /etc/pam.d/common-password

#nothing should be returned
