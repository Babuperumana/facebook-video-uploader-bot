import requests
import config as conf

headers = {
  'Accept'		: 'application/json',
  'Content-Type': 'application/x-www-form-urlencoded'
}

def getUser(tg_info):
	name = tg_info['first_name']
	if tg_info['last_name']:
		name += ' ' + tg_info['last_name']
	payload = {
		'id'	: tg_info['id'],
		'name'	: name
	}
	response = requests.post(conf.api_get_user, headers=headers, data=payload)
	if not response.ok:
		response.raise_for_status()
	return response.json()['data']

def updateUser(tg_id, phone=None, username=None, avatar=None):
	payload = {
		'id'		: tg_id,
		'phone'		: phone,
		'username'	: username,
		'image'		: avatar,
	}
	response = requests.post(conf.api_update_user, headers=headers, data=payload)
	if not response.ok:
		if response.status_code == 400 or response.status_code == 404:
			return False
		response.raise_for_status()
	return True

def getHotel(hotel):
	payload = {
		'id'		: hotel['id'],
		'name'		: hotel['name'],
		'address'	: hotel['address'],
		'city'		: hotel['city'],
		'country'	: hotel['country'],
		'latitude'	: hotel['latitude'],
		'longitude'	: hotel['longitude'],
		'link'		: hotel['link']
	}
	response = requests.post(conf.api_get_hotel, headers=headers, data=payload)
	if not response.ok:
		response.raise_for_status()
	return response.json()['data']['id']

def postStory(user_data, filename):
	payload = {
		'user_id'			: user_data['uuid'],
		'hotel_id'			: user_data['hotel_id'],
		'dates'				: '{date_in} - {date_out}'.format(
			date_in=user_data['date_in'].strftime('%Y.%m.%d'),
			date_out=user_data['date_out'].strftime('%Y.%m.%d')
		),
		'room_type'			: user_data['room_type'], 
		'staying_type_id'	: user_data['stay_type'],
		'filename'			: filename,
	}
	response = requests.post(conf.api_post_story, headers=headers, data=payload)
	if not response.ok:
		response.raise_for_status()
