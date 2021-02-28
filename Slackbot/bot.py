import slack
import os
from pathlib import Path
from dotenv import load_dotenv
#import flask
from flask import Flask
#handles events from slack
from slackeventsapi import SlackEventAdapter

#load the token from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#configure your flask application
app = Flask(__name__)

#configure SlackEventAdapter to handle events 
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)  #singing secret lets u read events from the channel

#using webclient in slack, there are other clients built-on as well !!
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

#handling message events
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text=text)  #connect the bot to the channel in the slack channel 

#run the 
if __name__ == "__main__":
    app.run(debug=True)