#!/usr/bin/env python

import SubintOSPFBGP

###########Inputs#################
##################################

#OSPF Interface
#R1 IP Address OSPF /30
IPadd_ospf_r1 = "192.168.1.1"

#R2 IP Address OSPF /30
IPadd_ospf_r2 = "192.168.1.2"

#OSPF Area
area_ospf = "0.0.0.0"

ospf_proc = "LAB-OSPF"

#BGP AS
local_as = "100"
remote_as = "200"

#BGP Peer
bgp_peer_r1 = "10.10.10.2"
bgp_peer_r2 = "10.10.10.6"

#BGP Interface
#R1 IP address BGP /30
IPadd_bgp_r1 = "10.10.10.1"

#R2 IP address BGP /30
IPadd_bgp_r2 = "10.10.10.5"


#Dot1Q
subint_1q_ospf_r1r2 = "100"
subint_1q_r1_bgp = "101"
subint_1q_r2_bgp = "102"


##################################
##################################

if __name__ == "__main__":
    
	SubintOSPFBGP.SubInt(subint_1q_ospf_r1r2, subint_1q_r1_bgp, IPadd_ospf_r1, IPadd_bgp_r1, "5000") #R1
	SubintOSPFBGP.ospfpayl(area_ospf, subint_1q_ospf_r1r2, ospf_proc, "5000")
	SubintOSPFBGP.bgppayl(remote_as, local_as, bgp_peer_r1, "5000")
	
	SubintOSPFBGP.SubInt(subint_1q_ospf_r1r2, subint_1q_r2_bgp, IPadd_ospf_r2, IPadd_bgp_r2, "5001") #R2
	SubintOSPFBGP.ospfpayl(area_ospf, subint_1q_ospf_r1r2, ospf_proc, "5001")
	SubintOSPFBGP.bgppayl(remote_as, local_as, bgp_peer_r2, "5001")