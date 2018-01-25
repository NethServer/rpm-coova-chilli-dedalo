# Example

#ifconfig $HS_LANIF 0.0.0.0
#iptables -t nat -A POSTROUTING -o $HS_WANIF -j MASQUERADE
#echo 1 > /proc/sys/net/ipv4/ip_forward
