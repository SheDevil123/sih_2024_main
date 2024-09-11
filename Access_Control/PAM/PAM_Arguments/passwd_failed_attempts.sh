grep -Pi -- '^\h*deny\h*=\h*[1-5]\b' /etc/security/faillock.conf
grep -Pi -- '^\h*auth\h+(requisite|required|sufficient)\h+pam_faillock\.so\h+([^#\n\r]+\h +)?deny\h*=\h*(0|[6-9]|[1-9][0-9]+)\b' /etc/pam.d/common-auth

#deny <= 5 
#nothing should be returned