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

(LANG, GREETINGS, HOTEL, DATE, ROOM, STAY, CONFIRM,
	VIDEO, USERNAME, PHONE, AVATAR, FINISH) = range(12)

user_data = {}

####################################

def error(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.error_msg[user_data[sender_id]['lang']]
	)

def askLanguage(sender_id, message=None):
	bot.send_button_message(
		sender_id,
		msg.ask_language,
		btn.language
	)
	user_data[sender_id]['conv_level'] = LANG

def getLanguage(sender_id, message):
	try:
		lang = message['postback']['payload']
		if lang in msg.languages:
			user_data[sender_id]['lang'] = lang
			return greetings(sender_id)
	except KeyError:
		pass
	return askLanguage(sender_id)

def greetings(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.greetings[user_data[sender_id]['lang']]
	)
	bot.send_button_message(
		sender_id,
		msg.starting[user_data[sender_id]['lang']],
		[ btn.add_hotel_button[user_data[sender_id]['lang']]]
	)
	user_data[sender_id]['conv_level'] = GREETINGS

def askHotel(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_hotel[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = HOTEL

def getHotel(sender_id, message=None):
	try:
		url = message['message']['attachments'][0]['url']
		# parse url
		return askDate(sender_id)
	except KeyError:
		return askHotel(sender_id)

def askDate(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_date[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = DATE

def askRoomType(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_room_type[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = ROOM

def askStayType(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_stay_type[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = STAY

def confirm(sender_id, message=None):
	bot.send_button_message(
		sender_id,
		msg.ask_confirm[user_data[sender_id]['lang']],
		[ btn.confirm_button[user_data[sender_id]['lang']] ]
	)
	user_data[sender_id]['conv_level'] = CONFIRM

def askVideo(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_video[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = VIDEO

def askUsername(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_username[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = USERNAME

def askPhone(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_phone[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = PHONE

def askAvatar(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.ask_avatar[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = AVATAR

def finish(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.finish[user_data[sender_id]['lang']]
	)
	user_data[sender_id]['conv_level'] = FINISH

####################################

conv_level_callbacks = {
	LANG		: getLanguage,
	GREETINGS	: askHotel,
	HOTEL		: getHotel,
	DATE		: askRoomType,
	ROOM		: askStayType,
	STAY		: confirm,
	CONFIRM		: askVideo,
	VIDEO		: askUsername,
	USERNAME	: askPhone,
	PHONE		: askAvatar,
	AVATAR		: finish,
	FINISH		: greetings,
}

def conversationHandler(message):
	sender_id = message['sender']['id']
	if not sender_id in user_data:
		user_data[sender_id] = {}

	#если диалог идёт, вызываем коллбэк следующего уровня диалога
	if 'conv_level' in user_data[sender_id]:
		conv_level = user_data[sender_id]['conv_level']
		conv_level_callbacks[conv_level](sender_id, message)
	#иначе если в постбэке есть старт, начинаем с вопроса о языке
	elif 'postback' in message:
		payload = message['postback']['payload']
		if payload == '/start':
			askLanguage(sender_id)

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
	app.run(debug=True)
