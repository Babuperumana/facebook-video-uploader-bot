import os
import sys
import requests
import flask
import boto3
from hashlib import md5
from io import BytesIO
from logging import getLogger, INFO, ERROR
from datetime import date, timedelta
from dateutil.parser import parse

from bot_class import Bot
from parse_link import parseUrl

import api_requests as api
import buttons as btn
import messages as msg
import config as conf

####################################

app = flask.Flask(__name__)
bot = Bot(conf.access_token)

logger = getLogger('main')

(LANG, START, HOTEL, DATES, ROOM, STAY, CONFIRM,
	VIDEO, USERNAME, PHONE, AVATAR, FINISH) = range(12)

user_data = {}

####################################

def lang(sender_id):
	try:
		return user_data[sender_id]['lang']
	except KeyError:
		return msg.default_language

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

def getAttachment(message):
	try:
		return message['message']['attachments'][0]
	except KeyError:
		return None

####################################

def askLanguage(sender_id):
	bot.send_quick_reply_message(
		sender_id,
		msg.ask_language,
		btn.language
	)
	logger.info('User connected - id: {}'.format(sender_id))
	user_data[sender_id]['conv_level'] = LANG

def getLanguage(sender_id, message):
	language = getPayload(message)
	if language not in msg.languages:
		return askLanguage(sender_id)
	user_data[sender_id]['lang'] = language
	return askToStart(sender_id)

def askToStart(sender_id, message=None):
	bot.send_text_message(
		sender_id,
		msg.greetings[lang(sender_id)]
	)
	bot.send_quick_reply_message(
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
	bot.send_action(sender_id, 'typing_on')
	try:
		hotel_data = parseUrl(getText(message))
	except Exception as err:
		bot.send_action(sender_id, 'typing_off')
		logger.error(str(err.args))
		return bot.send_text_message(
			sender_id,
			msg.link_error[lang(sender_id)]
		)
	bot.send_action(sender_id, 'typing_off')
	user_data[sender_id]['hotel'] = hotel_data
	bot.send_text_message(
		sender_id,
		msg.check_place[lang(sender_id)]
			.format(hotel_data['name'], hotel_data['address'])
	)
	return askDates(sender_id)

def askDates(sender_id):
	bot.open_webview(
		sender_id, 'dates',
		msg.ask_dates[lang(sender_id)],
		msg.pick_dates[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = DATES

def getDates(sender_id, message):
	date_in = parse(message.get('check_in'))
	date_out = parse(message.get('check_out'))
	if date_in > date_out:
		return bot.open_webview(
			sender_id, 'dates',
			msg.conflict_dates[lang(sender_id)],
			msg.pick_dates[lang(sender_id)]
		)
	dates = "{date_in} - {date_out}".format(
		date_in = date_in.strftime("%Y.%m.%d"),
		date_out = date_out.strftime("%Y.%m.%d")
	)
	user_data[sender_id]['dates'] = dates
	bot.send_text_message(
		sender_id,
		msg.check_dates[lang(sender_id)]
			.format(dates)
	)
	return askRoomType(sender_id)

def askRoomType(sender_id):
	bot.send_quick_reply_message(
		sender_id,
		msg.ask_room_type[lang(sender_id)],
		btn.roomsList(user_data[sender_id]['hotel']['rooms'])
	)
	user_data[sender_id]['conv_level'] = ROOM

def getRoomType(sender_id, message):
	room_type = getPayload(message)
	if not room_type:
		return askRoomType(sender_id)
	user_data[sender_id]['room_type'] = room_type
	bot.send_text_message(
		sender_id,
		msg.check_room[lang(sender_id)]
			.format(room_type)
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
		'{ask_confirm}\n{place}\n\n{dates}\n\n{room}\n\n{stay}'.format(
			ask_confirm=msg.ask_confirm[lng],
			place=msg.check_place[lng].format(
				ud['hotel']['name'], ud['hotel']['address']),
			dates=msg.check_dates[lng].format(ud['dates']),
			room=msg.check_room[lng].format(ud['room_type']),
			stay=msg.check_stay[lng].format(
				msg.stays[lng][ud['stay_type'] - 1])
		)
	)
	bot.send_quick_reply_message(
		sender_id,
		confirmation_message,
		btn.confirm_button[lng]
	)
	user_data[sender_id]['conv_level'] = CONFIRM

def getConfirm(sender_id, message):
	confirm = getPayload(message)
	if confirm != 'confirm':
		return confirm(sender_id)
	user_data[sender_id]['user_is_known'] = api.updateUser(sender_id)
	# user_from_db = api.getUser(bot.get_user_info(sender_id))
	# user_data[sender_id]['uuid'] = user_from_db['uuid']
	# user_data[sender_id]['username'] = user_from_db['username']
	# logger.info("Got user ID from API: {}"
	# 	.format(user_data[sender_id]['uuid']))
	# user_data[sender_id]['hotel_id'] = \
	# 	api.getHotel(user_data[sender_id]['hotel'])
	# logger.info("Got hotel ID from API: {}"
	# 	.format(user_data[sender_id]['hotel_id']))
	return askVideo(sender_id)

def askVideo(sender_id):
	bot.open_webview(
		sender_id, 'video',
		msg.ask_video[lang(sender_id)],
		msg.upload_video[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = VIDEO

def getVideo(sender_id, message):
	try:
		video = message['video']
	except KeyError:
		return bot.open_webview(
			sender_id, 'video',
			msg.not_a_video[lang(sender_id)],
			msg.upload_video[lang(sender_id)]
		)
	bot.send_action(sender_id, 'typing_on')
	logger.info('Got video from {}'.format(sender_id))
	video_hash = md5(video.read()).hexdigest()
	video.seek(0)
	filename = "{path}/{sender_id}_{dates}_{hash}.{extension}".format(
		path=conf.videos_path,
		sender_id=sender_id,
		dates=user_data[sender_id]['dates'],
		hash=video_hash,
		extension=video.filename.split('.')[-1]
	)
	# api.postStory(user_data[sender_id], filename)
	video.save(filename)

	# s3 = boto3.client('s3', **conf.aws_kwargs)
	# bucket_location = s3.get_bucket_location(Bucket=conf.bucket_name)
	# try:
	# 	video_bytes = BytesIO(video.read())
	# 	s3.upload_fileobj(
	# 		video_bytes, conf.bucket_name, filename,
	# 		ExtraArgs={'ACL':'public-read'}
	# 	)
	# except Exception as err:
	# 	log_level = ERROR
	# 	status_msg = 'Downloading failed because {}:\n{}'.format(
	# 		type(err).__name__, str(err.args))
	# else:
	# 	log_level = INFO
	# 	status_msg = 'Saved: https://s3-{}.amazonaws.com/{}/{}'.format(
	# 		bucket_location['LocationConstraint'],
	# 		conf.bucket_name, filename
	# 	)
	# logger.log(log_level, status_msg)

	bot.send_action(sender_id, 'typing_off')
	bot.send_text_message(
		sender_id,
		msg.video_thanks[lang(sender_id)]
	)
	if not user_data[sender_id]['user_is_known']:
		return askUsername(sender_id)
	return finish(sender_id)

def askUsername(sender_id):
	bot.send_text_message(
		sender_id,
		msg.ask_username[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = USERNAME

def getUsername(sender_id, message):
	username = getText(message)
	if not username:
		bot.send_text_message(
			sender_id,
			msg.wrong_username[lang(sender_id)]
		)
		return askUsername(sender_id)
	# username_is_unique = api.updateUser(
	# 	sender_id,
	# 	username=username
	# )
	# if not username_is_unique:
	# 	bot.send_text_message(
	# 		sender_id,
	# 		msg.duplicate_username[lang(sender_id)])
	# 	return askUsername(sender_id)
	user_data[sender_id]['username'] = username
	bot.send_text_message(
		sender_id,
		msg.username_success[lang(sender_id)]
			.format(username)
	)
	return askPhone(sender_id)

def askPhone(sender_id):
	bot.send_quick_reply_message(
		sender_id,
		msg.ask_phone[lang(sender_id)],
		btn.request_phone[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = PHONE

def getPhone(sender_id, message):
	phone = getPayload(message)
	if not phone:
		return bot.send_quick_reply_message(
			sender_id,
			msg.duplicate_phone[lang(sender_id)],
			btn.request_phone[lang(sender_id)]
		)
	user_data[sender_id]['user_is_known'] = True
	user_data[sender_id]['phone'] = phone.lstrip('+')
	# api.updateUser(
	# 	sender_id,
	# 	phone=user_data[sender_id]['phone']
	# )
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
		btn.skip_avatar[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = AVATAR

def getAvatar(sender_id, message):
	if getPayload(message) == 'skip':
		return finish(sender_id)
	bot.send_action(sender_id, 'typing_on')
	attachment = getAttachment(message)
	if not attachment or attachment['type'] != 'image':
		return askAvatar(sender_id)
	avatar_file = requests.get(attachment['payload']['url'])
	avatar_bytes = BytesIO()
	avatar_bytes.write(avatar_file.content)
	avatar_bytes.seek(0)
	filename = '{path}/{name}.{extension}'.format(
		path=conf.images_path,
		name=sender_id,
		extension=avatar_file.headers['Content-Type'].split('/')[-1]
	)

	with open(filename, 'wb+') as f:
		f.write(avatar_bytes.read())
	# boto3.client('s3', **conf.aws_kwargs).upload_fileobj(
	# 	avatar_bytes, conf.bucket_name,
	# 	'{path}/{filename}'.format(
	# 		path=conf.images_path, filename=filename),
	# 		ExtraArgs={'ACL':'public-read'}
	# )
	# api.updateUser(sender_id, avatar=filename)
	bot.send_action(sender_id, 'typing_off')
	return finish(sender_id)

def finish(sender_id):
	bot.send_text_message(
		sender_id,
		msg.finish[lang(sender_id)]
	)
	user_data[sender_id]['conv_level'] = FINISH
	del(user_data[sender_id])

####################################

next_level_callbacks = {
	LANG		: getLanguage,
	START		: getToStart,
	HOTEL		: getHotel,
	DATES		: getDates,
	ROOM		: getRoomType,
	STAY		: getStayType,
	CONFIRM		: getConfirm,
	VIDEO		: getVideo,
	USERNAME	: getUsername,
	PHONE		: getPhone,
	AVATAR		: getAvatar,
	FINISH		: askToStart,
}

back_button_callbacks = {
	LANG		: askLanguage,
	START		: askLanguage,
	HOTEL		: askToStart,
	DATES		: askHotel,
	ROOM		: askDates,
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
	del(user_data[sender_id])

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
	command = getPayload(message) or getText(message)
	try:
		commands_callbacks[command](sender_id)
	except KeyError:
		return False
	return True

def conversationHandler(message):
	sender_id = message['sender']['id']
	if not sender_id in user_data:
		user_data[sender_id] = {}
	try:
		if checkCommand(sender_id, message):
			return
		conv_level = user_data[sender_id]['conv_level']
		return next_level_callbacks[conv_level](sender_id, message)
	except KeyError:
		return askLanguage(sender_id)
	except Exception as err:
		logger.error(str(err.args))
		return error(sender_id)
	except KeyboardInterrupt:
		return stop(sender_id)

####################################

@app.route('/webhook', methods=['GET'])
def verifyToken():
	token_sent = flask.request.args.get('hub.verify_token')
	if token_sent != conf.verify_token:
		return flask.abort(403)
	return flask.request.args.get('hub.challenge')

@app.route('/webhook', methods=['POST'])
def receiveMessage():
	output = flask.request.get_json()
	for event in output['entry']:
		messaging = event['messaging']
		for message in messaging:
			conversationHandler(message)
	return flask.jsonify(success=True)

def withSenderID(func):
	def checkSenderID(*args, **kwargs):
		try:
			sender_id = flask.request.args.get('sender_id')
		except:
			flask.abort(403)
		if not sender_id in user_data:
			flask.abort(403)
		return func(sender_id, *args, **kwargs)
	checkSenderID.__name__ = func.__name__
	return checkSenderID

@app.route('/dates', methods=['GET'])
@withSenderID
def openDatesWebview(sender_id):
	today = date.today()
	return flask.render_template('datepicker.html',
		title=msg.dates_title[lang(sender_id)],
		sender_id=sender_id,
		ask_dates=msg.ask_dates[lang(sender_id)],
		pick_dates_btn=msg.pick_dates[lang(sender_id)],
		today=today.strftime('%Y-%m-%d'),
		max_date=(today + timedelta(days=100)).strftime('%Y-%m-%d')
	)

@app.route('/video', methods=['GET'])
@withSenderID
def openVideoWebview(sender_id):
	return flask.render_template('video_upload.html',
		sender_id=sender_id,
		upload_btn=msg.upload_video[lang(sender_id)],
	)

@app.route('/dates', methods=['POST'])
def getDatesFromWebview():
	data_func = getDates
	data_form = dict(flask.request.form)
	return processRequest(data_func, data_form)

@app.route('/video', methods=['POST'])
def getVideoFromWebview():
	data_func =	getVideo
	data_form = dict(flask.request.files)
	return processRequest(data_func, data_form)

def processRequest(data_func, data_form):
	sender_id = flask.request.form.get('sender_id')
	data_func(sender_id, data_form)
	return flask.redirect(
		"https://www.messenger.com/closeWindow/?display_text='{}'"
			.format(msg.close_window[lang(sender_id)])
	)

if __name__ == "__main__":
	app.run()
