nft list ruleset | awk '/hook input/,/}/' | grep 'iif "lo" accept'
nft list ruleset | awk '/hook input/,/}/' | grep 'ip saddr'
nft list ruleset | awk '/hook input/,/}/' | grep 'ip6 saddr'

#shouldreturn_lookbackinterfaceisconfig
#return_ipv4,ipv6lookbackinterface_drop

