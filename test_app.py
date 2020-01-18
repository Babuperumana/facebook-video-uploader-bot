import random
import os

from flask import Flask, request
from pymessenger.bot import Bot

import buttons as btn
import messages as msg
import config as conf

####################################

app = Flask(__name__)
bot = Bot(conf.access_token)

lang = 'ru'

(LANG, GREETINGS, HOTEL, DATE, ROOM, STAY, CONFIRM,
	VIDEO, USERNAME, PHONE, AVATAR, FINISH) = range(12)

def makeTmpButtons():
	for i in range(100):
		button = [{
			"type"		: "postback",
			"title"		: "Next",
			"payload"	: "/next{}".format(i)
		}]
		yield button

btn_generator = makeTmpButtons()

#поиграл с генератором кнопок

user_data = {}

####################################

def error(recipient_id):
	bot.send_text_message(recipient_id, msg.error_msg[lang])

def askLanguage(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_language, next(btn_generator))
	user_data[recipient_id]['conv_level'] = LANG

def greetings(recipient_id):
	bot.send_text_message(recipient_id, msg.greetings[lang])
	bot.send_button_message(recipient_id, msg.starting[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = GREETINGS

def askHotel(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_hotel[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = HOTEL

def askDate(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_date[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = DATE

def askRoomType(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_room_type[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = ROOM

def askStayType(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_stay_type[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = STAY

def confirm(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_confirm[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = CONFIRM

def askVideo(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_video[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = VIDEO

def askUsername(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_username[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = USERNAME

def askPhone(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_phone[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = PHONE

def askAvatar(recipient_id):
	bot.send_button_message(recipient_id, msg.ask_avatar[lang], next(btn_generator))
	user_data[recipient_id]['conv_level'] = AVATAR

def finish(recipient_id):
	bot.send_text_message(recipient_id, msg.finish[lang])
	user_data[recipient_id]['conv_level'] = FINISH

####################################

#по пэйлоаду вызываем callback 
conversation_functions = {
	'/start'	: askLanguage,
	'/next0'	: greetings,
	'/next1'	: askHotel,
	'/next2'	: askDate,
	'/next3'	: askRoomType,
	'/next4'	: askStayType,
	'/next5'	: confirm,
	'/next6'	: askVideo,
	'/next7'	: askUsername,
	'/next8'	: askPhone,
	'/next9'	: askAvatar,
	'/next10'	: finish,
}

def conversationHandler(message):
	if 'postback' in message:
		payload = message['postback']['payload']
		recipient_id = message['sender']['id']
		try:
			conversation_functions[payload](recipient_id)
		except KeyError:
			error(recipient_id)

####################################

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
				conversationHandler(message)
		return 'good'

def verifyToken(token_sent):
	if token_sent == conf.verify_token:
		return request.args.get("hub.challenge")
	return 'Invalid verification token'

if __name__ == "__main__":
	app.run()
