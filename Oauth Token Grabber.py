from O365 import Account
from O365 import Connection
# Replace client_id and client_secret with your Azure App
credentials = ('azure_client_id', 'azure_client_secret')
#------------------------------------
#Assing these permissions to Azure App
#  https://graph.microsoft.com/Mail.Read
#  https://graph.microsoft.com/Mail.ReadWrite
#  https://graph.microsoft.com/Mail.Send
#  https://graph.microsoft.com/User.Read
#--------------------------------------
account = Account(credentials)
if account.authenticate(scopes=['basic', 'message_all']):
   print('Authenticated!')

