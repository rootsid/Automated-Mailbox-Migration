# Automated-Mailbox-Migration
Automated Staged Mailbox Migration

Welcome to Automated Staged Mailbox Migration, Never need a team now just launch on one of Mail Servers and it will handle everything on it's own.

Project is still under development almost ready in peices, send your merge requests if you want to contribute.

To check csv files for email list via a mailbox create a app on Azure.

Authentication

You can only authenticate using oauth athentication as Microsoft deprecated basic auth on November 1st 2018.

There are currently two authentication methods:

Authenticate on behalf of a user: Any user will give consent to the app to access it's resources. This oauth flow is called authorization code grant flow. This is the default authentication method used by this library.

Authenticate with your own identity: This will use your own identity (the app identity). This oauth flow is called client credentials grant flow.

'Authenticate with your own identity' is not an allowed method for Microsoft Personal accounts.

When to use one or the other and requirements:

Topic	On behalf of a user (auth_flow_type=='authorization')	With your own identity (auth_flow_type=='credentials')
Register the App	Required	Required
Requires Admin Consent	Only on certain advanced permissions	Yes, for everything
App Permission Type	Delegated Permissions (on behalf of the user)	Application Permissions
Auth requirements	Client Id, Client Secret, Authorization Code	Client Id, Client Secret
Authentication	2 step authentication with user consent	1 step authentication
Auth Scopes	Required	None
Token Expiration	60 Minutes without refresh token or 90 days*	60 Minutes*
Login Expiration	Unlimited if there is a refresh token and as long as a refresh is done within the 90 days	Unlimited
Resources	Access the user resources, and any shared resources	All Azure AD users the app has access to
Microsoft Account Type	Any	Not Allowed for Personal Accounts
Tenant ID Required	Defaults to "common"	Required (can't be "common")
*O365 will automatically refresh the token for you on either authentication method. The refresh token lasts 90 days but it's refreshed on each connection so as long as you connect within 90 days you can have unlimited access.

The Connection Class handles the authentication.

Oauth Authentication
This section is explained using Microsoft Graph Protocol, almost the same applies to the Office 365 REST API.
