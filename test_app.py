import random
import os

from flask import Flask, request
from pymessenger.bot import Bot

import buttons as btn
import config as conf

app = Flask(__name__)
bot = Bot(conf.access_token)

@app.route("/", methods=['GET', 'POST'])
def receiveMessage():
	if request.method == 'GET':
		token_sent = request.args.get("hub.verify_token")
		return verifyToken(token_sent)
	else:
		output = request.get_json()
		print(output)
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
				#Facebook Messenger ID for user so we know where to send response back to
					recipient_id = message['sender']['id']
					if message['message'].get('text'):
						response_sent_text = get_message()
						send_message(recipient_id, response_sent_text)
					#if user sends us a GIF, photo,video, or any other non-text item
					if message['message'].get('attachments'):
						response_sent_nontext = get_message()
						send_message(recipient_id, response_sent_nontext)
	return "Message Processed"

def verifyToken(token_sent):
	if token_sent == conf.verify_token:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'

#chooses a random message to send to the user
def get_message():
	sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
	# return selected item to the user
	return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
	#sends user the text message provided via input response parameter
	bot.send_button_message(recipient_id, "test", btn.navigation)
	bot.send_text_message(recipient_id, response)
	return "success"

if __name__ == "__main__":
	app.run()
