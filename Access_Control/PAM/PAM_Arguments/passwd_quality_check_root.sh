grep -Psi -- '^\h*enforce_for_root\b' /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf
#eg output
#/etc/security/pwquality.conf.d/50-pwroot.conf:enforce_for_root