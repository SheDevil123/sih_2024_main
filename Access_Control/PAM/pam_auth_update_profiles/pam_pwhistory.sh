grep -P -- '\bpam_pwhistory\.so\b' /etc/pam.d/common-password

# password requisite pam_pwhistory.so remember=24 enforce_for_root try_first_pass use_authtok