####################################################	
## Mail Checker                                   ##	
####################################################	

##################################	
## Written by: Sidharth Kaushik ##	
##  root@sidharthkaushik.com    ##	
##################################
from O365 import Account
from O365 import Connection
import os
import time
import subprocess
credentials = ('Azure_client_id', 'Azure_client_secret')

account = Account(credentials)
mailbox = account.mailbox()

inbox = mailbox.inbox_folder()
query = inbox.q().on_attribute('subject').contains('migration')
for message in inbox.get_messages(query=query):
    output = open(r'output.txt','a+')
    if os.path.exists("new_subjects.txt"):
      os.remove("new_subjects.txt")
    else:
      pass
    print(message, file=output)
    output.close()

out_set = set([line.rstrip('\n') for line in open('output.txt')])
proc_set = set([line.rstrip('\n') for line in open('processed.txt')])
new_subjects = open(r'new_subjects.txt','a+')
diff = out_set - proc_set
new_subjects.writelines("%s\n" % unique for unique in diff)
new_subjects.close()
os.remove("output.txt")
    
with open("new_subjects.txt") as fp:
    processed = open(r'processed.txt','a+')
    new_subject = fp.readline()
    new_subject = new_subject.rstrip("\n\r")
    print(new_subject, file=processed)
    processed.close()
