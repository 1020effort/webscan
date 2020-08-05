#!/usr/bin/python
#coding=utf-8
import re
import requests
import sys
from forestyle import *
from colorama import Fore

timeout = 5

def endswith(str):
    if not str.endswith("/"):
        str += "/"
    return str

def redfore(str):
    print(Fore.RED + str + Fore.RESET)

def greenfore(str):
    print(Fore.GREEN + str + Fore.RESET)

def yellowfore(str):
    print(Fore.YELLOW + str + Fore.RESET)
	
def bluefore(str):
    print(Fore.BLUE + str + Fore.RESET)
	
def magentafore(str):
    print(Fore.MAGENTA + str + Fore.RESET)
	
def cyanfore(str):
    print(Fore.CYAN + str + Fore.RESET)

def havebak(str):
    restr = ''
    f = open('bak.txt','r')
    line = f.readline()[:-1]
    while line:
        if(str.find(line)>=0):
            restr = line
            f.close()
            return restr
        line = f.readline()[:-1]
    f.close()
    return restr

def geturl(url):
    request = requests.get(url,timeout=timeout)
    if(request.status_code == 200):
        cyanfore('[+]DIRECTORY==>' + url + ' [200 OK]')
        optstr = optionsurl(url)
        if len(optstr)>0:
            print '   [-]OPTIONS:',
            optstr = optionsurl(url)
        if(optstr.find('PUT')>=0):
            redfore(optstr)
        else:
            print(optstr)
        bakfile = havebak(request.text)
        if(len(bakfile)>0):
            redfore('   [-]Found maybe backup file ['+bakfile+']')
    if(request.status_code == 302):
        print '[+]' + url,
        cyanfore(' [302]')

def getfile(url):
    request = requests.get(url,timeout=timeout)
    restr = request.text
    if(request.status_code == 200):
        greenfore('[+]FILE=>' + url + ' [200 OK]')
        sourcescan(restr)
    expandscan(url)

def getexpend(url):
    request = requests.get(url,timeout=timeout)
    if(request.status_code == 200):
        redfore('[+]FILE BAK=>' + url + '[200 OK]')

def regstr(regs,str):
    r = re.search(regs,str,re.IGNORECASE)
    if(r != None):
        redfore('   view-source:have hide message,show view-source get more message! one of them:['+ r.group(0) +']')

def sourcescan(str):
    regstr('<!--(.*)-->',str)
    regstr('<!flag(.*)>',str)
    if(str.find('<?php')>=0 or str.find('&lt;?php')>=0):
        redfore('   view-source:maybe include source code!')

def expandscan(url):
    f = open('expand.txt','r')
    line = f.readline()[:-1]
    while line:
        getexpend(url + line)
        line = f.readline()[:-1]
    f.close()

def optionsurl(url):
    request = requests.options(url,timeout=timeout)
    try:
        return(request.headers['Allow'])
    except:
        return ''

def checkhead(url):
    request = requests.get(url,timeout=timeout)
    try:
        for key,value in request.headers.items():
            if(key=='Server' or key=='X-Powered-By'):
                yellowfore(key + ':' + value)
            elif(key.find('flag')>=0):
                redfore(key + ':' + value)
            else:
                print(key + ':' + value)
        #cyanfore(request.headers)
        #yellowfore('Server:'+request.headers['Server'])
        #yellowfore('X-Powered-By:'+request.headers['X-Powered-By'])
    except:
        return 'Get Headers error!'

def dirscan():
    f = open('dir.txt','r')
    line = endswith(f.readline()[:-1])
    while line:
        geturl(website + line)
        line = f.readline()[:-1]
    f.close()

def filescan():
    f = open('file.txt','r')
    line = f.readline()[:-1]
    while line:
        getfile(website + line)
        line = f.readline()[:-1]
    f.close()
print('')
print('EffortScan v1.0')
print('--------------------------------------------')
try:
    website = endswith(sys.argv[1])
except:
    print('python effortscan.py [url] | need parameter!')
    print('eg: python effortscan.py http://www.baidu.com')
    sys.exit(0)
magentafore('---- Scanning URL: ' + website + ' ----')
print('--------------------------------------------')
checkhead(website)
getfile(website)
dirscan()
filescan()
yellowfore('---- Scan End ----')
