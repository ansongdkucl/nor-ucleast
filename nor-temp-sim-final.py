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

    inlet_int = int(inlet)
    if inlet_int > 45:
        message = {'text': bot_string}
        #webhook for temp breach channel#
        url = "https://liveuclac.webhook.office.com/webhookb2/55fbc416-3229-443c-80b8-3ae51b69765f@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/0dfeb0f55f834f5dabf37eef5b124b9c/43bfe760-7689-4d0b-96fd-46b265519580"
        response_body = requests.post(url=url,data=json.dumps(message))
        print(response_body)
     


    message = {'text': bot_string}

    print(message)
      

    #url = 'https://liveuclac.webhook.office.com/webhookb2/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/204db79c2042430a85ad7e03bbcc9d29/43bfe760-7689-4d0b-96fd-46b265519580'
    url = 'https://liveuclac.webhook.office.com/webhookb2/55fbc416-3229-443c-80b8-3ae51b69765f@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/2b83566ca510452c8249c35733232c4d/43bfe760-7689-4d0b-96fd-46b265519580'

 
    response_body = requests.post(url=url,data=json.dumps(message))
    print(response_body)
     

def main() -> None:
    nr = InitNornir(config_file='/home/dansong/scripts/ucle/config.yaml')
    voip = nr.filter(F(building=444))
    result = voip.run(task=dev_info)

if __name__ == '__main__':
    main()
