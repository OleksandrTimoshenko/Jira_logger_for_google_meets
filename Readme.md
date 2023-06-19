# This code will transfer your rallies to your Jira
(If you set it up correctly and your Jira is set up the same way as the author's )

## Google cloud setup
1. Create a new app in [Google](https://console.cloud.google.com/projectcreate) (it is better to use personal e-mail...)

2. Go to the Library  
find the Google Calendar API and enable it

3. Go to the "QAyth contest" screen  
App Name - random  
User email - mine  
Developer contact information - also my email  
Then just click on "Back to dashboard"   
Do not forget to enable the app!

4. Go to the credentials tab  
Click on "Create credentials"  
Select "OAuth client ID"  
Selekt type - "Deckpot app" - in our case  
Name - random  
Upload the file with credentials and store it in ./creds.json


## Jira setup

After logging to your Jira go to "Profile" -> "Personal Access Tokens" and create a new one

## Create .env file
```
mkdir creds
cp creds.json ./creds/creds.json
cp .env.example ./creds/.env
```
Provide all credentials in .env file

## Start using
```
python3 ./main.py --help
```