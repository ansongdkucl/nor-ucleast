from unittest import result
from urllib import response
from nornir import InitNornir
import json
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from nornir_netmiko.tasks import netmiko_send_config
from nornir.core.filter import F
import requests
import csv
import re


temp_list = []


def dev_info(task):
    r = task.run(netmiko_send_command, command_string="show env temperature status | inc Inlet", use_genie=True)
    task.host["facts"] = r.result
    #print(task.host)
    r_string = r.result
    #print(r_string)
   
    inlet = re.search(r'\d+',r_string).group()
    #print(inlet)

    r5 = task.run(netmiko_send_command, command_string="show snmp location",enable=True)
    snmp_str = r5.result
    bot_string = '{}{} {}'.format(inlet,'°',snmp_str)
    print(bot_string)




    message = {'text': bot_string}

    print(message)
      

    url = 'https://liveuclac.webhook.office.com/webhookb2/55fbc416-3229-443c-80b8-3ae51b69765f@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/27205071d2e84b46b3c0c273e260741f/43bfe760-7689-4d0b-96fd-46b265519580'
 
    response_body = requests.post(url=url,data=json.dumps(message))
    print(response_body)
     

def main() -> None:
    nr = InitNornir(config_file='/home/dansong/scripts/ucle/config.yaml')
    voip = nr.filter(F(cab=13))
    result = voip.run(task=dev_info)

if __name__ == '__main__':
    main()
