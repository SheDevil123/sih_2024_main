systemctl list-unit-files | awk '$1~/^crond?\.service/{print $2}'
systemctl list-units | awk '$1~/^crond?\.service/{print $3}'

#enabled
#active
