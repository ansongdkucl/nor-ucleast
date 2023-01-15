import subprocess
import json
import requests
import re
import threading


down = []
ips = []

pat = '(\d+.\d+.\d+.\d+)(\s+)(.*)'

def openFile():
    global ip_list
    with open('/home/dansong/scripts/lists/qsh_list.txt') as f:
        data = f.read()
        words = data.split('\n')
        ips.append(words)
        ip_list = ips[0]
        return ip_list
    
def get_ip(ip_list,x):
    status = True
    while status:
        thread_count = 100

        hostData = re.search(pat,str(x))
        try:

            ip = hostData.group(1)
            des = hostData.group(3)
        except:
            #print('could not process this',ip)
            pass
        #print(ip)
        
        ret = subprocess.call(['ping', '-c', '1', '-W', '1', '{}'.format(ip)],
        stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        #ret = subprocess.call(['ping', '-n', '4', '{}'.format(ip)])

        
        if ret == 0:
            print('{}\t {} ----- online'.format(ip,des))
            
            if ip in down:
                down.remove(ip)
                url = 'https://liveuclac.webhook.office.com/webhookb2/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/fa406716f3e54ec59323dbaff585c821/43bfe760-7689-4d0b-96fd-46b265519580'
                message = {
                    'text': '{} is back ONLINE'.format(ip)
                }
                response_body = requests.post(url=url,data=json.dumps(message))
            
    
        else:
            print('{} {} is offline'.format(ip,des))    
            print('These devices are down--',down)
                
            if ip not in down:
                down.append(ip)
                #url =  'https://liveuclac.webhook.office.com/webhookb2/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/fa406716f3e54ec59323dbaff585c821/43bfe760-7689-4d0b-96fd-46b265519580'  
                url =  'https://liveuclac.webhook.office.com/webhookb2/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/c4e7dd2078d44df587cc0719b26bdd6a/43bfe760-7689-4d0b-96fd-46b265519580'      
                #url = 'https://outlook.office.com/webhook/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/8e7c75766f034b2785ebd72aa70a61bd/43bfe760-7689-4d0b-96fd-46b265519580'
                #url = 'https://outlook.office.com/webhook/259922d6-28bb-4426-ac14-a44f8da775b9@1faf88fe-a998-4c5b-93c9-210a11d9a5c2/IncomingWebhook/59011a10e8f545f08f369f25967bd404/43bfe760-7689-4d0b-96fd-46b265519580'
                message = {
                    'text': '{} {}  ----- OFFLINE'.format(ip, des)
                }
                response_body = requests.post(url=url,data=json.dumps(message))

        
                    

def main():
    openFile()
    threads = []
    for x in ip_list:
        t = threading.Thread(target=get_ip, args=(ip_list,x,)) 
        t.start()

        # Wait for all threads to complete
    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()



if __name__ == "__main__":
    main()  
    

    
        
    
        





