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

    #r = task.run(netmiko_send_config, config_commands=["vlan 18","name 10.11.18.0/24_Audiocodes"])
    #r = task.run(netmiko_send_config, config_commands=["int range te1/1/1 - 4","sw trunk allowed vlan add 18"])
    r = task.run(netmiko_send_config, config_commands=["service timestamps debug datetime localtime show-timezone",
    "service timestamps debug datetime localtime show-timezone"])
    content = r.result
    print(content)


nr = InitNornir(config_file='/home/dansong/scripts/auto-vlan/config.yaml')
#voip = nr.filter(F(building=2) | F(building=388))
voip = nr.filter(F(building=388))
result = voip.run(name='change snmp',task=find)       




'''
WS-3650-PD Te1/1/3-4 
WS-3650-48QFM Te1/1/1 - 4 
C9300L-48PF-4X Te1/1/1 - 4
WS-2960X-48FPD-L Te1/0/1 -2 

'''