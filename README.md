# What is this?

Script that checks the current time and uses the content API for shopping to 
switch the feed fetch schedule in Google Shopping according to the time of day. 
A crude half day feed fetch time switcher. 

# Installation Instructions
 - pip install -r requirements.txt
 
 # Setup Instructions
 Set up a project in the Google Cloud Console and create a service account credential. 
 Save the credential file as 'service-account.json' and store it in the /credentials 
 directory. Run main.py on a schedule.