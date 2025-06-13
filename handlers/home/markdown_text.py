markdown_text = """
# **Goal**

- Minimize the interaction with Keep Secure 24 
- Have a centralize application that perform most of the administrative task we daily face.

# **Authentication**

#### ***Disclaimer***
The application is suppose to run on our Windows machine. All the secrets will be saved into a 
Window Credentials Manager.

Technically it will work als on Linux (GNOME Keyring or KWallet) and macOS (Keychain).

- Keep Secure API Key
- AI API Key
- Google Desktop Auth

### ***Keep Secure and AI API Keys***

These are saved directly into the Window Credentials Manager. No much to add

### ***Google Desktop Auth***

This is not the classic service account of Google.
These are credentials that allows a Desktop application (third party) to interact with Google service. 
In our case mainly Drive.
The application, that is not published but is a testing state, by default it does allow only the tester to utilize 
these credentials for interact with the Google service.

##### ***How does it work?***

The first time the application call a Google service, a browser it will open for Google authentication.
If the user that authenticate in Google is part of the tester, will be allowed to utilize the service otherwise Google 
will not allow.

The json file is encode in base64 and saved in the Window Credentials Manager. In the moment of bne utilize, 
it get decode, a temporary json is created and utilized for authenticate in Google, and after that destroy.

After the first time authenticating, the app will create a token, for avoid authenticate in the future.
The time to live of the token is strictly relate to the time to live of the password, once the password is changed 
the token is invalid.
Alternative the token can be deleted manually

# **Upload vulnerability**

- Utilize a standard template to fetch the finding note.
- The note should contains at the first page, Organisation, Asset and Test uuid, the following for each finding Title, 
Severity, Note and Images.
- The note can be load from local storage or google drive.

Once load the application try to match, based on the title, the finding to a vulnerability type.
For the ones the match is not possible the user can manually add the vulnerability type.

All the notes are send, along with the relate template of the vulnerability type, to the AI assistance, that utilize 
the information in the note and in the template for build a description, and impact an recommendation. 
The template information are the baseline for all of three sections.
It will suggest some reference (NOT VERIFY THE LINK)
Not all Vulnerability types as template, not all template are complete.
If the template is missing or some part of it is missing the AI Assistant will fill in the rest accordingly.

Once return the response, is still possible to modify the AI Assistance response before to upload the finding.
All the finding are upload along the with the images in a Ready to Publish state.

# **Test**

Function that allow to insert into the Test details on Keep Secure 24, all the necessary information needed for 
reporting.

# **Publish and delete Vulnerability**

Function that allow to publish or delete single vulnerability or more vulnerability within the same test.
The requirement for publish a vulnerability is that the "state" is set on Ready to be Publish.
This can't be set via API

# **Migration**

Manage the migration of one or more vulnerability within a specific test to global.
This it will automatically create, and publish the vulnerability in the specific Global Asset, and delete the original 
from the market.

# **Reporting**

It generate slide and pdf for the finding meeting and the report.
At the moment it save both locally.
"""
