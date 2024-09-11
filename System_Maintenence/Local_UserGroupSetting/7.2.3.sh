#!/usr/bin/env bash

# Ensure running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Extract unique GIDs
mapfile -t a_passwd_group_gid < <(awk -F: '{print $4}' /etc/passwd | sort -u)
mapfile -t a_group_gid < <(awk -F: '{print $3}' /etc/group | sort -u)

# Find GIDs in /etc/passwd that are not in /etc/group
a_passwd_group_diff=($(comm -23 <(printf '%s\n' "${a_passwd_group_gid[@]}" | sort) <(printf '%s\n' "${a_group_gid[@]}" | sort)))

# Check users with missing GIDs
for l_gid in "${a_passwd_group_diff[@]}"; do
  awk -F: '($4 == '"$l_gid"') {print " - User: \"" $1 "\" has GID: \""$4 "\" which does not exist in /etc/group" }' /etc/passwd
done

# Clean up
unset a_passwd_group_gid; unset a_group_gid; unset a_passwd_group_diff

