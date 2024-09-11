grep -P -- '\bpam_faillock\.so\b' /etc/pam.d/common-{auth,account}

# /etc/pam.d/common-auth:auth requisite
# pam_faillock.so preauth
# /etc/pam.d/common-auth:auth [default=die]
# pam_faillock.so authfail
# /etc/pam.d/common-account:account required
# pam_faillock.so