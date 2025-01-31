import requests
import os

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
# CHANNEL is the channel that the bot will post to. This is the channel that the bot will post to when the bot is run on a job & called in main.py. 
CHANNEL = '#fintech-general-body-slack'
# TESTING_CHANNEL is the channel that is used for testing purposes and is only run when slack_sender.py is run directly.
TESTING_CHANNEL = 'test-bot'

def send_slack_message(message, slack_token, slack_channel):
    """Send a message to Slack using the OAuth token.
    
    :message: The message to send to Slack.
    :slack_token: The OAuth token for the Slack bot.
    :slack_channel: The channel to send the message to.
    """
    headers = {
        'Authorization': f'Bearer {slack_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': slack_channel,
        'text': message
    }
    response = requests.post('https://slack.com/api/chat.postMessage', json=data, headers=headers)
    return response.json()


if __name__ == "__main__": 
    message = 'Hello! This is a test message from the Slack bot.'
    clean_summary = '\n'.join(line.strip() for line in message.split('\n'))
    formatted_message = f"""
    
    Hello everyone! Here's what's going on in finance/tech today…

    {clean_summary}

    * Note from Head of Tech: Like all LLMs, this bot can make mistakes.
    * This bot will post on Tuesdays & Thurdays around 3 PM EST."""
    
    result = send_slack_message(formatted_message, SLACK_BOT_TOKEN, TESTING_CHANNEL)
    print(result)