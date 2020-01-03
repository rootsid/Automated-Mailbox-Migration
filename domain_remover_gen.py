import re
import csv
import os
import subprocess,sys
import getpass
import pyautogui
import time
#---------------------------------------------
#EOP
#---------------------------------------------
print(r"(+) Please enter your User ID for on-prem either with @domain.com or Domain\Username")
on_prem_user_id = input()
print("Got it")
print("(+) Please enter your password for on-premise exchange")
print("(+) Enter password carefully as I've not updated program to validate LDAP")
on_prem_password = getpass.getpass(prompt='Password: ', stream=None)
print("Got it")
print("(+) Please enter on-prem url address in form of http://<ServerFQDN>/PowerShell/ ")
on_prem_url_in = input()
on_prem_connect = "$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri " + on_prem_url_in + " -Authentication Kerberos -Credential $UserCredential"
#---------------------------------------------
def connect_on_prem():
    p = subprocess.Popen([r"powershell.exe"],
    creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(5.5)
    pyautogui.typewrite('$UserCredential = Get-Credential')
    pyautogui.press('enter')
    pyautogui.typewrite(on_prem_user_id, interval=0.001)
    pyautogui.press('tab')
    pyautogui.typewrite(on_prem_password,interval=0.001)
    pyautogui.press('enter')
    pyautogui.typewrite(on_prem_connect,interval=0.001)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.typewrite("Import-PSSession $Session -DisableNameChecking", interval=0.001)
    pyautogui.press('enter')
    time.sleep(20)
#---------------------------------------------
connect_on_prem()    
pyautogui.typewrite(r"Import-csv MigrationEmails.csv | ForEach-Object {Get-Mailbox -Identity $_.MigrationEmail | Select-Object UserPrincipalName,emailaddresses } | Export-csv migration.csv -NoTypeInformation",interval = 0.001)
pyautogui.press('enter')
time.sleep(5)
os.popen("taskkill /IM powershell.exe >nul")
print("(+)---------------------------------------------(+)")
print("(+)Generating File Now(+)")
print("(+)---------------------------------------------(+)")
#---------------------------------------------
migration = open(r'migration.csv','r')
csv_reader = csv.reader(migration, delimiter=',')
proxyaddress = []
primaryemails = []
unique_emails = []
bad_emails = []
for row in csv_reader:
    rows = str(row)
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", rows)
    for email in emails:
        if 'microsoft' in email:
            proxyaddress.append(email)
        elif '@' in email:
            primaryemails.append(email)
pe = map(lambda x:x.lower(),primaryemails)
pe = list(set(pe))
for item in pe:
    unique_emails.append(item)
accepted = open(r"accepted.txt",'r',encoding='UTF-16')
accepted_emails = accepted.read()
for domain in proxyaddress:
    emails = domain.split('@')[1]
    if emails not in accepted_emails:
        bad_emails.append(domain)
##sorting valid emails
accepted_proxy = re.findall("([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", accepted_emails)
for accepted_paddress in accepted_proxy:
    if "onmicrosoft.com" in accepted_paddress:
        accepted_proxy_stamp = accepted_paddress
if os.path.exists("validemails.csv"):
        os.remove("validemails.csv")
else:
    pass
with open(r'validemails.csv','a+',newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(["primaryemail","proxyaddress"])
    for domain in unique_emails:
        emails = domain.split('@')[0]
        writer.writerow([domain,emails+"@"+accepted_proxy_stamp])
file.close()
##invalid emails
if os.path.exists("process.csv"):
    os.remove("process.csv")
else:
    pass
with open(r'process.csv','a+',newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(["primaryemail","proxyaddress"])
    for email in unique_emails:
        em = email.split('@')[0]
        for bad_email in bad_emails:
            if em in bad_email.lower():
                writer.writerow([email,bad_email])
            pass
file.close()
print("(+)Generated(+)")
print("(+)---------------------------------------------(+)")
time.sleep(30)
connect_on_prem()
pyautogui.typewrite(r"Import-csv process.csv | foreach {Set-Mailbox -Identity $_.primaryemail -EmailAddresses @{remove=$_.proxyaddress}}",interval = 0.001)
pyautogui.press('enter')
time.sleep(30)
pyautogui.typewrite(r"Import-csv validemails.csv | foreach {Set-Mailbox -Identity $_.primaryemail -EmailAddresses @{add=$_.proxyaddress}}",interval = 0.001)
pyautogui.press('enter')
time.sleep(30)
os.popen("taskkill /IM powershell.exe >nul")
input('Press enter to quit* ')
