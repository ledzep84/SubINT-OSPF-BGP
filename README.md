# SubINT-OSPF-BGP<br>
Off-box creation of Sub-interface, OSPF neighbor, BGP peer for automation in IOS-XR
<br><br>
Uses:
- ncclient Python library as a NETCONF client
- Cisco YANG model for:
  - Sub-interface creation
  - OSPF neighbor configuration
- Openconfig YANG model for:
  - BGP peer configuration<br><br><br>
  
  All sample variables can be edited in main.py<br><br>
  
  Files:<br>
  main.py - Main python script<br>
  SubintOSPFBGP.py - Functions for configuring the box<br>
  
  Tested in:<br>
  Ubuntu 16.04<br>
  Python 2.7
  
