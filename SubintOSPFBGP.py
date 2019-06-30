#!/usr/bin/env python

from ncclient import manager
#Functions to:
#Create Subinterface
#Initiate an OSPF and BGP neighborship
#Modify the host, port, user, pass, etc

def SubInt(subint1qospfr1r2, subint1qrbgp, IPaddospfr, IPaddbgpr, portvar):
    with manager.connect(host="localhost", port=portvar, username="cisco", password="cisco", hostkey_verify=False, device_params={'name': 'iosxr'}, allow_agent=False, look_for_keys=False) as iosxr:
		subintconf = """
		<config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
		 <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
		  <interface-configuration>
		   <active>act</active>
		   <interface-name>GigabitEthernet0/0/0/1</interface-name>
		   <description>Inter-Router</description>
		  </interface-configuration>
		  <interface-configuration>
		   <active>act</active>
		   <interface-name>GigabitEthernet0/0/0/1.{ospfint_var}</interface-name>
		   <interface-mode-non-physical>default</interface-mode-non-physical>
		   <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
		    <addresses>
		     <primary>
		      <address>{ipospf_var}</address>
		      <netmask>255.255.255.252</netmask>
		     </primary>
		    </addresses>
		   </ipv4-network>
		   <vlan-sub-configuration xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2-eth-infra-cfg">
		    <vlan-identifier>
		     <vlan-type>vlan-type-dot1q</vlan-type>
		     <first-tag>{ospfint_var}</first-tag>
		    </vlan-identifier>
		   </vlan-sub-configuration>
		  </interface-configuration>
		  <interface-configuration>
		   <active>act</active>
		   <interface-name>GigabitEthernet0/0/0/2</interface-name>
		   <description>To BGP Peer</description>
		  </interface-configuration>
		  <interface-configuration>
		   <active>act</active>
		   <interface-name>GigabitEthernet0/0/0/2.{bgpint_var}</interface-name>
		   <interface-mode-non-physical>default</interface-mode-non-physical>
		   <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
		    <addresses>
		     <primary>
		      <address>{ipbgp_var}</address>
		       <netmask>255.255.255.252</netmask>
		     </primary>
		    </addresses>
		   </ipv4-network>
		   <vlan-sub-configuration xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-l2-eth-infra-cfg">
		    <vlan-identifier>
		     <vlan-type>vlan-type-dot1q</vlan-type>
		     <first-tag>{bgpint_var}</first-tag>
		    </vlan-identifier>
		   </vlan-sub-configuration>		   
		  </interface-configuration>
		 </interface-configurations>
		</config>
		""".format(ospfint_var = subint1qospfr1r2, bgpint_var = subint1qrbgp, ipospf_var = IPaddospfr, ipbgp_var = IPaddbgpr)

		iosxr_reply = iosxr.edit_config(target='candidate', config = subintconf)
		iosxr.commit()
    return        


def ospfpayl(areaospf, subint1qospfr1r2, procname, portvar):
    with manager.connect(host="localhost", port=portvar, username="cisco", password="cisco", hostkey_verify=False, device_params={'name': 'iosxr'}, allow_agent=False, look_for_keys=False) as iosxr:
		ospfconf = """
         <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
          <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-ospf-cfg">
           <processes>
            <process>
             <process-name>{proc_name}</process-name>
             <default-vrf>
              <area-addresses>
               <area-address>
                <address>{ospfarea}</address>
                <running/>
                <name-scopes>
                 <name-scope>
                  <interface-name>GigabitEthernet0/0/0/1.{ospfint_var}</interface-name>
                  <running/>
                  <network-type>point-to-point</network-type>
                 </name-scope>
                </name-scopes>
               </area-address>
              </area-addresses>
             </default-vrf>
             <start/>
            </process>
           </processes>
          </ospf>
         </config>
		""".format(ospfarea = areaospf, ospfint_var = subint1qospfr1r2, proc_name = procname)

		iosxr_reply = iosxr.edit_config(target='candidate', config = ospfconf)
		iosxr.commit()
    return

def bgppayl(remoteas, localas, bgppeer, portvar):
	with manager.connect(host="localhost", port=portvar, username="cisco", password="cisco", hostkey_verify=False, device_params={'name': 'iosxr'}, allow_agent=False, look_for_keys=False) as iosxr:
		bgpconf = """
		<config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
		 <bgp xmlns="http://openconfig.net/yang/bgp">
		  <global>
		   <config>
			<as>{aslocal}</as>
		   </config>
		   <afi-safis>
			<afi-safi>
			 <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:ipv4-unicast</afi-safi-name>
			 <config>
			  <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:ipv4-unicast</afi-safi-name>
			  <enabled>true</enabled>
			 </config>
			</afi-safi>
		   </afi-safis>
		  </global>
		  <neighbors>
		   <neighbor>
			<neighbor-address>{peerbgp}</neighbor-address>
			<config>
			 <neighbor-address>{peerbgp}</neighbor-address>
			 <peer-as>{asremote}</peer-as>
			</config>
			<afi-safis>
			 <afi-safi>
			  <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:ipv4-unicast</afi-safi-name>
			  <config>
			   <afi-safi-name xmlns:idx="http://openconfig.net/yang/bgp-types">idx:ipv4-unicast</afi-safi-name>
			   <enabled>true</enabled>
			  </config>
			  <apply-policy>
			   <config>
			    <import-policy>PASS</import-policy>
			    <export-policy>PASS</export-policy>
			   </config>
			  </apply-policy>
			 </afi-safi>
			</afi-safis>
		   </neighbor>
		  </neighbors>
		 </bgp>
		</config>
		""".format(asremote = remoteas, aslocal = localas, peerbgp = bgppeer)
		iosxr_reply = iosxr.edit_config(target='candidate', config = bgpconf)
		iosxr.commit()
	return
