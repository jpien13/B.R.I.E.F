# B.R.I.E.F
Brown's Relevant Intelligence Engine for Fintech

## Testing Locally

### Setting up Virtual Environment
This codebase assumes you are using a virtual environment (venv). This is a good practice to avoid dependency conflicts. To create a virtual environment, run the following command in the root directory of the project: 
```
python3 -m venv venv
```
To activate the virtual environment, run the following command: 
```
source venv/bin/activate
```
To deactivate the virtual environment, run the following command: deactivate

Next, you will have to install all the project dependancies. I have collected all the library dependancies you would need in the requirements.txt file. To install all the dependancies, run the following command: 
```
pip install -r requirements.txt
```
You should be all set up with the venv now.

### Getting your Google 16 char Password Authentication

Google has deprecated the use of passwords for logging in to Gmail. Instead, you will need to use a 16 character password that you generate from your Google Account. To do this, go to your Google Account, then go to Security, then go to App Passwords. You will need to select the app and device you are using to generate the password. Once you have generated the password, you will need to use that password in the code.

1.  Go to https://myaccount.google.com
2.  Sign in with your Google Account credentials. DO NOT USE SCHOOL EMAIL. Brown blocks this feature so you will have to use a personal email.
3. Click 'Security'
4. Scroll to "2-Step Verification" and click on it. You may need to enable 2-Step Verification if you haven't already.
5. Enter password if prompted
6. Once 2-Step Verification is enabled, go back to security and at the top in the searchbar, search for "App Passwords" and click on it.
7. Give a name to your App, I just name it BREIF. A screen will pop up for your generated app password. This is shown in a format like: ```xxxx xxxx xxxx xxxx```. It will be 16 characters long, 19 including spaces. Copy this down somewhere safe.
8. Once you have copied this down somewhere safe, you can close the tab.
9. You will need to use this 16 character password in the code instead of your normal password. This 16 character password is what you will use as your EMAIL_PASSWORD environment variable in the next section. 

### Setting up Environment Variables
The code expects all passwords, emails, and API keys to be environment varibles (secrets) in the GitHub workflow. This is for obvious security reasons. We wouldnt want your email, password, or keys to be leaked from a public repo :( As such, you will need to set these up locally to test the code. The following are the secrets that need to be set as environemtn variables:

This assumes you are on Mac OS and sets the temporary environment variables for the email address and password.
```
export EMAIL_ADDRESS="your.email@gmail.com"
```
```
export EMAIL_PASSWORD="your_16_character_password"
```
If you wanted permanent environment variables, you would need to add them to your .bash_profile or .zshrc file. This is not recommended for security reasons. If you are on Windows, you would need to set these as environment variables in the System Properties.

Next, you need to set up the slack bot OAUTH as an environment variable. If the bot is not already created, then to get this OAUTH key, you first need to actually create the bot in slack's app. 

1. Go to this website and click 'create new app' : ```https://api.slack.com/apps```
2. Click create from scrath
3. Give your bot/app a name and select the desire workspace and click create
4. After creating the app, navigate to the "OAuth & Permissions" section. Scroll down to the "Scopes" section and add the following scope under Bot Token Scopes: ```chat:write``` – This allows the app to post messages to Slack channels.
5. Once you've added the necessary permissions, install the app to your workspace by clicking the Install to Workspace button. After installation, you’ll get a Bot User OAuth Token. This token will be used in your Python script to authenticate API requests. Write this token down somewhere safe. After you have written it down, you can set it as an environment variable in your terminal by typing:

```
export SLACK_BOT_TOKEN="your slack token"
```

6. Next, go to the channel you want to post to and invite the bot to the channel. You can do this by typing /invite @your_bot_name in the channel and selecting the bot from the list.
7. Lastly, in ```slack_sender.py``` set the global variable ```CHANNEL``` to the channel you want to post to; its just the channel name. For example #fintech-general-body-slack. Additionally, if you want to test the bot without posting to a public channel, you can set the ```TESTING_CHANNEL``` to another channel and run slack_sender.py directly. This will post to the testing channel instead of the public channel assuming you made another private channel on slack to test on.

Ok last step. The general way this bot works, is that it expects a email newsletter and parses that into a slack message. The email newsletter is expected to be in the form of a html file. Essentailly, it summarizes a newsletter sent to the EMAIL_ADDRESS you entered as an environment variable and summarizes it and sends to slack. If you are looking for a webscraping bot, check out T.I.D.A.L on my git jpien13. Although, I believe this approach is better given the difficulties of webscraping and 403 Forbidden errors. Back to my point. Since this bot uses a newsletter, you need to be subscribed to a daily newsletter you want the bot's content to pull from. Once you have done so, add that sender gmail addresss as an enivronment variable called ```SENDER```.


```
export SENDER_EMAIL="example_newsletter@newsletter.com"
```

One thing to note, you should be aware of approximately what time the newsletter sends their daily emails. For example, the one I use gets the email roughly around 2:30 pm every weekday. So in my yml file, I set the job to run automatically everday at 3:00 pm wver weekday, slightly after the expected time of arriveal from the newsletter.