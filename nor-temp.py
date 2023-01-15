from unittest import result
from nornir import InitNornir
import json
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from nornir_netmiko.tasks import netmiko_send_config
from nornir.core.filter import F
import requests
import csv
import re


def dev_info(task):
    r = task.run(netmiko_send_command, command_string="show env temperature status | inc Inlet", use_genie=True)
    task.host["facts"] = r.result
    #print(task.host)
    r_string = r.result
   
    inlet = re.search(r'\d+',r_string).group()
    print(inlet)

    r5 = task.run(netmiko_send_command, command_string="show snmp location",enable=True)
    snmp_str = r5.result


    if 20 < int(inlet) < 56:
        print('Test Please ignore')
        message = {
        'text': 'IGNORE TESTING--- \n Yellow Threshold Breach for {} \n location:\n {} '
        .format(task.host,snmp_str)}
        url = 'https://liveuclac.webhook.office.com/webhookb2/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/204db79c2042430a85ad7e03bbcc9d29/43bfe760-7689-4d0b-96fd-46b265519580'
        response_body = requests.post(url=url,data=json.dumps(message))
    
    if int(inlet) > 56:
        print('IGNORE TESTING--- \n Red Threshold Breach for {} \n location:\n {} '.format(task.host,snmp_str))
        url = 'https://liveuclac.webhook.office.com/webhookb2/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/204db79c2042430a85ad7e03bbcc9d29/43bfe760-7689-4d0b-96fd-46b265519580'
                    
        message = {
            'text':'Yellow Threshold Breach for {} location:\n{} '.format(task.host,snmp_str)
            }
    
        response_body = requests.post(url=url,data=json.dumps(message))





def main() -> None:
    nr = InitNornir(config_file='/home/dansong/scripts/ucle/config.yaml')
    voip = nr.filter(F(building=445))
    result = voip.run(task=dev_info)
    #print_result(result)

if __name__ == '__main__':
    main()
