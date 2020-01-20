import random
import os

from flask import Flask, request
from bot_class import Bot

import buttons as btn
import messages as msg
import config as conf

####################################

app = Flask(__name__)
bot = Bot(conf.access_token)

(LANG, START, HOTEL, DATE, ROOM, STAY, CONFIRM,
	VIDEO, USERNAME, PHONE, AVATAR, FINISH) = range(12)

user_data = {}

####################################

def lang(sender_id):
	try:
		return user_data[sender_id]['lang']
	except KeyError:
		return 'ru'

def getText(message):
	try:
		return message['message']['text']
	except KeyError:
		return None

def getPayload(message):
	try:
		return message['message']['quick_reply']['payload']
	except KeyError:
		pass
	try:
		return message['postback']['payload']
	except KeyError:
		pass
	return None

####################################

def askLanguage(sender_id):
	bot.send_quick_reply_message(
		sender_id,
		msg.ask_language,
		btn.language
	)
	user_data[sender_id]['conv_level'] = LANG

def getLanguage(sender_id, message):
	language = getPayload(message)
	if language not in msg.languages:
		return askLanguage(sender_id)
	user_data[sender_id]['lang'] = lang
	return askToStart(sender_id)

def askToStart(sender_id):
	bot.send_text_message(
		sender_id,
		msg.greetings[lang(sender_id)]
	)
	bot.send_button_message(
		sender_id,
		msg.starting[lang(sender_id)],
		btn.add_hotel[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = START

def getToStart(sender_id, message):
	payload = getPayload(message)
	if payload != 'add':
		return bot.send_button_message(
			sender_id,
			msg.ask_again[lang(sender_id)],
			btn.add_hotel[lang(sender_id)]
		)
	return askHotel(sender_id)

def askHotel(sender_id):
	bot.send_text_message(
		sender_id,
		msg.ask_hotel[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = HOTEL

def getHotel(sender_id, message):
	try:
		url = message['message']['attachments'][0]['url']
	except KeyError:
		url = getText(message)
	# parse url
	hotel_data = url
	if not hotel_data:
		return bot.send_text_message(
			sender_id,
			msg.link_error[lang(sender_id)]
		)
	user_data[sender_id]['hotel'] = hotel_data
	bot.send_text_message(
		sender_id,
		msg.check_place[lang(sender_id)]
			.format(hotel_data)
	)
	return askDate(sender_id)

def askDate(sender_id):
	bot.send_text_message(
		sender_id,
		msg.ask_date[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = DATE

def getDate(sender_id, message):
	date = getText(message)
	#parse date
	parsed_date = date
	if not parsed_date:
		return askDate(sender_id)
	user_data[sender_id]['date'] = parsed_date
	bot.send_text_message(
		sender_id,
		msg.check_date[lang(sender_id)]
			.format(parsed_date)
	)
	return askRoomType(sender_id)

def askRoomType(sender_id):
	bot.send_text_message(
		sender_id,
		msg.ask_room_type[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = ROOM

def getRoomType(sender_id, message):
	room_type = getText(message)
	if not room_type:
		return askRoomType(sender_id)
	user_data[sender_id]['room_type'] = room_type
	bot.send_text_message(
		sender_id,
		msg.check_room[lang(sender_id)]
	)
	return askStayType(sender_id)

def askStayType(sender_id):
	bot.send_quick_reply_message(
		sender_id,
		msg.ask_stay_type[lang(sender_id)],
		btn.stay_types[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = STAY

def getStayType(sender_id, message):
	stay_type = getPayload(message)
	if not 'stay' in stay_type:
		return askStayType(sender_id)
	stay_type = int(stay_type[-1])
	user_data[sender_id]['stay_type'] = stay_type
	bot.send_text_message(
		sender_id,
		msg.check_stay[lang(sender_id)]
			.format(msg.stays[lang(sender_id)][stay_type - 1])
	)
	return askConfirm(sender_id)

def askConfirm(sender_id):
	ud = user_data[sender_id]
	lng = lang(sender_id)
	confirmation_message = (
		'{ask_confirm}\n{place}\n\n{date}\n\n{room}\n\n{stay}'.format(
			ask_confirm=msg.ask_confirm[lang],
			place=msg.check_place[lng].format(ud['hotel']),
			date=msg.check_date[lng].format(ud['date']),
			room=msg.check_room[lng].format(ud['room_type']),
			stay=msg.check_stay[lng].format(
				msg.stays[lng][ud['stay_type'] - 1])
		)
	)
	bot.send_button_message(
		sender_id,
		confirmation_message,
		btn.confirm_button[lng]
	)
	user_data[sender_id]['conv_level'] = CONFIRM

def getConfirm(sender_id, message):
	confirm = getPayload(message)
	if confirm != 'confirm':
		return confirm(sender_id)
	return askVideo(sender_id)

def askVideo(sender_id):
	bot.send_text_message(
		sender_id,
		msg.ask_video[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = VIDEO

def getVideo(sender_id, message):
	video = getText(message)
	if not video:
		return bot.send_text_message(
			sender_id,
			msg.not_a_video[lang(sender_id)]
		)
	#api call to save video
	#if user is registered:
	#	return finish(sender_id)
	bot.send_text_message(
		sender_id,
		msg.video_thanks[lang(sender_id)]
	)
	return askUsername(sender_id)

def askUsername(sender_id):
	bot.send_text_message(
		sender_id,
		msg.ask_username[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = USERNAME

def getUsername(sender_id, message):
	username = getText(message)
	#check username
	if not username:
		return bot.send_text_message(
			sender_id,
			msg.wrong_username[lang(sender_id)]
		)
	user_data[sender_id]['username'] = username
	bot.send_text_message(
		sender_id,
		msg.username_success[lang(sender_id)]
			.format(username)
	)
	return askPhone(sender_id)

def askPhone(sender_id):
	bot.send_text_message(
		sender_id,
		msg.ask_phone[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = PHONE

def getPhone(sender_id, message):
	phone = getText(sender_id)
	#check_phone
	if not phone:
		return bot.send_text_message(
			sender_id,
			msg.duplicate_phone[lang(sender_id)]
		)
	user_data[sender_id]['phone'] = phone
	bot.send_text_message(
		sender_id,
		msg.check_phone[lang(sender_id)]
			.format(phone)
	)
	return askAvatar(sender_id)

def askAvatar(sender_id):
	bot.send_quick_reply_message(
		sender_id,
		msg.ask_avatar[lang(sender_id)],
		btn.skip_button[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = AVATAR

def getAvatar(sender_id, message):
	if getPayload(sender_id) == 'skip':
		return finish(sender_id)
	avatar = getText(sender_id)
	#check avatar
	if not avatar:
		return askAvatar(sender_id)
	return finish(sender_id)

def finish(sender_id):
	bot.send_text_message(
		sender_id,
		msg.finish[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = FINISH

####################################

next_level_callbacks = {
	LANG		: getLanguage,
	START		: getToStart,
	HOTEL		: getHotel,
	DATE		: getDate,
	ROOM		: getRoomType,
	STAY		: getStayType,
	CONFIRM		: getConfirm,
	VIDEO		: askUsername,
	USERNAME	: askPhone,
	PHONE		: askAvatar,
	AVATAR		: finish,
	FINISH		: askToStart,
}

back_button_callbacks = {
	LANG		: askLanguage,
	START		: askLanguage,
	HOTEL		: askToStart,
	DATE		: askHotel,
	ROOM		: askDate,
	STAY		: askRoomType,
	CONFIRM		: askStayType,
	VIDEO		: askConfirm,
	USERNAME	: askVideo,
	PHONE		: askUsername,
	AVATAR		: askPhone,
	FINISH		: askAvatar,
}


def error(sender_id):
	bot.send_text_message(
		sender_id,
		msg.error_msg[lang(sender_id)]
	)

def stop(sender_id):
	bot.send_text_message(
		sender_id,
		msg.conv_ended[lang(sender_id)]
	)
	user_data[sender_id].pop('conv_level', None)

def back(sender_id):
	try:
		conv_level = user_data[sender_id]['conv_level']
	except KeyError:
		conv_level = LANG
	return back_button_callbacks[conv_level](sender_id)

commands_callbacks = {
	'/start'	: askLanguage,
	'/stop'		: stop,
	'/home'		: askToStart,
	'/back'		: back,
}

def checkCommand(sender_id, message):
	try:
		command = message['postback']['payload']
	except KeyError:
		try:
			command = message['message']['text']
		except KeyError:
			return False
	try:
		commands_callbacks[command](sender_id)
	except KeyError:
		return False
	return True

def conversationHandler(message):
	sender_id = message['sender']['id']
	if not sender_id in user_data:
		user_data[sender_id] = {}

	if not checkCommand(sender_id, message):
		try:
			conv_level = user_data[sender_id]['conv_level']
		except KeyError:
			return error(sender_id)
		else:
			return next_level_callbacks[conv_level](sender_id, message)

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
