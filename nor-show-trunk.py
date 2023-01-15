from nornir import InitNornir
import re
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.tasks.files import write_file
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from nornir_netmiko.tasks import netmiko_send_config
from nornir.core.filter import F

import csv

def find(task):
    print(task.host)
    r = task.run(netmiko_send_command, command_string="show ver | inc Model (N|n)umber", enable=True)
    content = r.result
    print(content)
    return content
   

nr = InitNornir(config_file='/home/dansong/scripts/auto-vlaconfig.yaml')
voip = nr.filter(F(building=111))
result = voip.run(name='change snmp',task=find)




'''
snmp-server view ALL-ACCESS iso included
snmp-server group network-admin v3 priv read ALL-ACCESS access 23
snmp-server user snmp-solarwinds network-admin v3 auth sha <<removed, ask me>> priv aes 128 <<removed, ask me>>

 

ip access-list standard 22
1 permit 10.28.12.0 0.0.0.255
2 permit 10.36.12.0 0.0.0.255
ip access-list resequence 22 10 10

 

ip access-list standard 23
1 permit 10.28.12.0 0.0.0.255
2 permit 10.36.12.0 0.0.0.255
ip access-list resequence 23 10 10
'''

 