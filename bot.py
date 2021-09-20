import slack
import os

client = slack.WebClient(token = '####')

client.chat_postMessage(channel = '#sector-materials', text='Hello World!')