import requests
import os
import random
import json
import threading
import sys

from random_username.generate import generate_username
from colorama import init, Fore
init()

def main():
    os.system('cls')

    def successful(username, password, cookie):
        sys.stdout.write(Fore.GREEN + "(+) Successfully created account! Check accounts.txt for details.")
        open('accounts.txt', 'w').write(''+ username +':'+ password +':'+ cookie +'')

    def captcha():
        sys.stdout.write(Fore.RED + "(-) Failed to create an account due to captcha!\n")

    def toomanyrequests():
        sys.stdout.write(Fore.RED + "(-) Failed to create an account due to rate-limits!\n")

    cookie = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_3BB915038549A71C23881F12FB5333DB8D602C18A1BD5B56714BB61B97463F29EEC1488021763212A01CFB6554AB481E66F5E8AF87092408AD8844D873C21B7FA358C08FEDD4392DDD862C5C46C417F287336A798E2BC61E56124326FBE4732077CFA5D944C4EBB00A76A8EC43D97F9215E2CE002908BF18F50D4480B958CEC2B4C8720071AD2CC4C5DAD1381F12394369DCB50A3BC4234AF1945D28AE7CFA0B810B8C3973CACCE31BF4997C530AD03990F2999341EA6DA4E466CADCC45D51436BC2FB289334616B2CFBA34456CA7ACD09C5B83AD723A1DAD4CF7CBDE0C5FD56F3224CBA859D7E8313148D922B71F2DD7EB33621C9D0BD5BD8F1123C589D15678A15405D8DC519C2698848B109F3E05B214EE869AB86B638809D16D2BD9D2FEAA284858829FF26B1E239D771827D8FEA0B3B2D30A8D648D257545A3F6C2DA37D7A4AAF4BDBEE46FC6F611A3B089DACCFE74C926F'

    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie

    req = session.post(
        url="https://auth.roblox.com/"
    )

    if 'X-CSRF-TOKEN' in req.headers:
        session.headers['X-CSRF-TOKEN'] = req.headers['X-CSRF-TOKEN']

    proxy = random.choice(open('proxies.txt').read().splitlines())
    
    def post():
        name = generate_username(1)[0] 
        signupJson = {
            "username": name,
            "password": name + 'PASS',
            "gender": "Unknown",
            "birthday": "1999-11-15T04:40:28.901Z",
            "captchaId": "",
            "captchaToken": "",
            "captchaProvider": ""
        }

        while True:
            b = session.post('https://auth.roblox.com/v2/signup', json=signupJson, headers={'Content-Type': 'application/json', 'X-CSRF-TOKEN': session.headers['X-CSRF-TOKEN']}, proxies={'http': 'http://'+ proxy +''})
            parsed = json.loads(b.text)
            
            if parsed['errors'][0]['code'] is 0:
                toomanyrequests()
            elif parsed['errors'][0]['code'] is 2:
                captcha()
            else:
                successful(name, name+'PASS', cookie)

    threads = []

    for i in range(30):
        t = threading.Thread(target=post)
        t.daemon = True
        threads.append(t)

    for i in range(30):
        threads[i].start()

    for i in range(30):
        threads[i].join()



if __name__ == "__main__":
    main()
