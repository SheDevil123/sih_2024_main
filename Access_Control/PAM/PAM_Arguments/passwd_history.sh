grep -Psi -- '^\h*password\h+[^#\n\r]+\h+pam_pwhistory\.so\h+([^#\n\r]+\h+)?remember=\d+\b ' /etc/pam.d/common-password

# password requisite pam_pwhistory.so remember=24 enforce_for_root
# try_first_pass use_authtok