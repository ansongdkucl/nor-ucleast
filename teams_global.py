from nornir import InitNornir
import re
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from nornir_netmiko.tasks import netmiko_send_config
from nornir.core.inventory import Group
import time
import pysnmp
import smtplib
import datetime
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from nornir.core.filter import F
import json
import requests
import sys


# Email variables
fromaddr = "d.ansong@ucl.ac.uk"
toaddr = ["d.ansong@ucl.ac.uk"]
server = smtplib.SMTP('smtp-server.ucl.ac.uk', 587)

interfaces = []
venMAC = ['a85b.f7']
#venMAC = ['b.8221']
#venMAC = ['000b.8']

def find(task):
    #prints each target hostname
    print(task.host.name)
    #tm_vlan = voip.inventory.hosts[task.host.name]
    tm_vlan = nr.inventory.hosts[task.host.name]
   

    for mac_add in venMAC:
        r = task.run(netmiko_send_command, command_string="show mac add | inc {}".format(mac_add),enable=True)
        content = r.result
        #print(content)

        if mac_add in content:
            #regex to capture all interface paterns  
            int_pat = re.findall(r'Te\d\/\d+\/\d+|Gi\d\/0\/\d+|fa0\/\d+',content)
            
            #regex to capture mac addressers
            mac_pat = re.findall(r'([0-9a-z]{4}[\.][0-9a-z]{4}[\.][0-9a-z]{4})',content)
            
            #Remove duplicates from list 'pat' and create new list 'interfaces
            interfaces = list(set(int_pat))
            
            #print('Devices Found on {} on {}'.format(task.host,interfaces))     
            
            for dev in interfaces:
                r1 = task.run(netmiko_send_command, command_string="show int status | inc {}".format(dev),enable=True)        
                #print(r1.result)

                if 'trunk' in r1.result:
                    #Exits program script if interface is a trunk port
                    #print("port is trunk no action taken")
                    sys.exit()
    
                else:              
                    r2 = task.run(netmiko_send_command, command_string="show run int {} | inc voice".format(dev),enable=True)
                    #print(r2.result)
                    
                    #strip extrace white spaces from sting
                    sw_string = r2.result.lstrip()   
                    
                  
                    string_1 = 'switchport voice vlan {}'.format(tm_vlan['voip'])
                    #print(sw_string)
                    #print(string_1)

                    #if the correct voice vlan on port no action taken
                    if string_1 == sw_string:
                        print(tm_vlan,dev,'device already on the on the voice vlan')
                        break
                      
                    else:
                        print('change vlan on',tm_vlan,dev)

                        r4 = task.run(netmiko_send_command, command_string="show mac address-table int {}".format(dev),enable=True)
                        content = r4.result
                        mac_pat1 = re.findall(r'([0-9a-z]{4}[\.][0-9a-z]{4}[\.][0-9a-z]{4})',content)
                        #remove duplicates form list
                        mac_pat2 = list(set(mac_pat1))
                        print(mac_pat2)
                        
                        r3 = task.run(netmiko_send_config, config_commands=["int {}".format(dev),"switchport voice vlan {}".format(tm_vlan['voip']),
                        "no trust device cisco-phone","no auto qos voip cisco-phone","wr mem","shut","no shut"])
                        print('Voice vlan added')

                        time.sleep(1)

                        r5 = task.run(netmiko_send_command, command_string="show snmp location",enable=True)
                        snmp_str = r5.result

                        msg = MIMEMultipart()
                        msg['From'] = fromaddr
                        msg['To'] = ",".join(toaddr)

                        msg['Subject'] = 'MS Teams Config'
                        body = f"The following device has been configured below:\n"
                        body += f"\n{snmp_str}"
                        body += f"\n\nMac: {mac_pat2}"
                        body += f"\nswitch: {task.host.name}"
                        body += f"\nport: {dev}"
                        body += f"\nvlan: {tm_vlan['voip']}"
                    
                        print(body)

                        msg.attach(MIMEText(body, 'plain'))
                        text = msg.as_string()
                        server.sendmail(fromaddr, toaddr, text)

                        #Sends webhook to my Teams Channel
                        url = 'https://liveuclac.webhook.office.com/webhookb2/2cfe4a0c-d741-4cc5-9ee7-863ffc3a7531@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/17eae3044f9c42868f4a0598aafa925b/43bfe760-7689-4d0b-96fd-46b265519580'
                        # Sends webhook to Vlan Changes Teams Channel
                        #url = 'https://liveuclac.webhook.office.com/webhookb2/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/8dbdbb64f2c144f7b485cd823fd0ae27/43bfe760-7689-4d0b-96fd-46b265519580'
                        message = {
                            'text': 'The following device has been configured below:\\\n {} \\\n Mac {}\\\nSwitch {}\\\n port {} \\\n vlan {}'
                            .format(snmp_str,mac_pat2,task.host.name,dev,tm_vlan['voip'])
                            
                        }
                        response_body = requests.post(url=url,data=json.dumps(message))


#nr = InitNornir(config_file='/home/ansongdk/projects/nornir-projects/auto-vlan/config.yaml')
nr = InitNornir(config_file='/home/dansong/scripts/auto-vlan/config.yaml')
#voip = nr.filter(F(building=2577))
voip = nr.filter(F(building=51))
result = voip.run(name='find mac address',task=find)