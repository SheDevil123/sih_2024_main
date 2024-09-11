sshd -T | grep -Pi -- '^\h*(allow|deny)(users|groups)\h+\H+'

# allowusers <userlist>
# -OR-
# allowgroups <grouplist>
# -OR-
# denyusers <userlist>
# -OR-
# denygroups <grouplist>