# Automated-Mailbox-Migration
Automated Staged Mailbox Migration

Welcome to Automated Staged Mailbox Migration, never need a team now just launch on one of Mail Servers and it will handle everything on its own.

Project is still under development almost ready in pieces, send your merge requests if you want to contribute.

To check csv files for email list via a mailbox create a app on Azure.

Authentication

You can only authenticate using oauth authentication as Microsoft deprecated basic auth on November 1st 2018.

There are currently two authentication methods:

* Authenticate on behalf of a user: Any user will give consent to the app to access it's resources. This oauth flow is called authorization code grant flow. This is the default authentication method used by this library.

* Authenticate with your own identity: This will use your own identity (the app identity). This oauth flow is called client credentials grant flow.

'Authenticate with your own identity' is not an allowed method for Microsoft Personal accounts.

When to use one or the other and requirements:


Topic
On behalf of a user (auth_flow_type=='authorization')
With your own identity (auth_flow_type=='credentials')
Register the App
Required
Required
Requires Admin Consent
Only on certain advanced permissions
Yes, for everything
App Permission Type
Delegated Permissions (on behalf of the user)
Application Permissions
Auth requirements
Client Id, Client Secret, Authorization Code
Client Id, Client Secret
Authentication
2 step authentication with user consent
1 step authentication
Auth Scopes
Required
None
Token Expiration
60 Minutes without refresh token or 90 days*
60 Minutes*
Login Expiration
Unlimited if there is a refresh token and as long as a refresh is done within the 90 days
Unlimited
Resources
Access the user resources, and any shared resources
All Azure AD users the app has access to
Microsoft Account Type
Any
Not Allowed for Personal Accounts
Tenant ID Required
Defaults to "common"
Required (can't be "common")


*O365 will automatically refresh the token for you on either authentication method. The refresh token lasts 90 days but it's refreshed on each connection so as long as you connect within 90 days you can have unlimited access.

The Connection Class handles the authentication.

Oauth Authentication

1. This section is explained using Microsoft Graph Protocol, almost the same applies to the Office 365 REST API.

To allow authentication you first need to register your application at Azure App Registrations.
1. Login at Azure Portal (App Registrations)
2. Create an app. Set a name.
3. In Supported account types choose "Accounts in any organizational directory and personal Microsoft accounts (e.g. Skype, Xbox, Outlook.com)", if you are using a personal account.
4. Set the redirect uri (Web) to: https://login.microsoftonline.com/common/oauth2/nativeclient and click register. This needs to be inserted into the "Redirect URI" text box as simply checking the check box next to this link seems to be insufficent. This is the default redirect uri used by this library, but you can use any other if you want.
5. Write down the Application (client) ID. You will need this value.
6. Under "Certificates & secrets", generate a new client secret. Set the expiration preferably to never. Write down the value of the client secret created now. It will be hidden later on.
7. Under Api Permissions:
* When authenticating "on behalf of a user":
1. add the delegated permissions for Microsoft Graph you want (see scopes).
2. It is highly recommended to add "offline_access" permission. If not the user you will have to re-authenticate every hour.
* When authenticating "with your own identity":
1. add the application permissions for Microsoft Graph you want.
2. Click on the Grant Admin Consent button (if you have admin permissions) or wait until the admin has given consent to your application.
As an example, to read and send emails use:
3. Mail.ReadWrite
4. Mail.Send
5. User.Read



2. Then you need to login for the first time to get the access token that will grant access to the user resources.

To authenticate (login) you can use different authentication interfaces. On the following examples we will be using the Console Based Interface but you can use any one.

* When authenticating on behalf of a user:
1.Instantiate an Account object with the credentials (client id and client secret).
2.Call account.authenticate and pass the scopes you want (the ones you previously added on the app registration portal).


Note: when using the "on behalf of a user" authentication, you can pass the scopes to either the Account init or to the authenticate method. Either way is correct.


You can pass "protocol scopes" (like: "https://graph.microsoft.com/Calendars.ReadWrite") to the method or use "scope helpers" like ("message_all"). If you pass protocol scopes, then the account instance must be initialized with the same protocol used by the scopes. By using scope helpers you can abstract the protocol from the scopes and let this library work for you.
Finally, you can mix and match "protocol scopes" with "scope helpers". Go to the procotol section to know more about them.

Scope Helper | Scopes included
------------ | ---------------
basic        | 'offline_access' and 'User.Read'
mailbox      | 'Mail.Read'
mailbox_shared |'Mail.Read.Shared'
message_send | 'Mail.Send'
message_send_shared |'Mail.Send.Shared'
message_all |'Mail.ReadWrite' and 'Mail.Send'


#<h1>Mail Check

Subjects will be compared once a migration will be processed that will be added in processed file for logs and future comparison to check new migration emails in Mailbox.

#<h1>Domain Fixer

In case of multiple bad proxy domains or company takeover bad proxy domains or any invalid smtp address’s which are not in Accepted Domains List will be removed and correct proxy address will be stamped.

#<h1>Migration Batch

After all preliminary checks a migration batch will be created and will be monitored in backend to check for any errors if any errors will come all will be fixed and batch will be resumed.

If completion time is specified in the email then that will be considered otherwise migration will be auto completed.

After Completion of Batch an email will be triggered to Mailbox which you will provide in the beginning with GRAPH API.
