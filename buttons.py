import messages as msg

language = [
	{
		'content_type'	: 'text',
		'title'			: msg.pick_language[lang],
		'payload'		: lang
	} for lang in msg.languages
]

#navigation
btn_home = {
	lang : {
		'type'		: 'postback',
		'title'		: msg.home_button[lang],
		'payload'	: '/home'
		} for lang in msg.languages
}

btn_back = {
	lang : {
		'type'		: 'postback',
		'title'		: msg.back_button[lang],
		'payload'	: '/back'
		} for lang in msg.languages
}

navigation = {
	'persistent_menu': [
		{
			'locale': locale,
			'composer_input_disabled': False,
			'call_to_actions': [
				btn_home[lang],
				btn_back[lang]
			]
		} for lang, locale in msg.languages.items()
	] + [
		{
			'locale': 'default',
			'composer_input_disabled': False,
			'call_to_actions': [
				btn_home[msg.default_language],
				btn_back[msg.default_language]
			]
		}
	]
}
#####

#start
add_hotel = {
	lang : [
		{
			'content_type'	: 'text',
			'title'			: msg.add_place[lang],
			'payload'		: 'add'
		}
	]
	for lang in msg.languages
}
#####

#room type
def roomsList(rooms_list):
	return [
		{
			'content_type'	: 'text',
			'title'			: room,
			'payload'		: room,
		} for _, room in zip(range(13), rooms_list)
	]
# max 13 buttons are allowed by facebook api
#####

#stay types
stay_types = {
	lang : [
		{
			'content_type'	: 'text',
			'title'			: stay_type,
			'payload'		: 'stay{}'.format(index)
		} for index, stay_type in enumerate(msg.stays[lang])
	] for lang in msg.languages
}

#confirm
confirm_button = {
	lang : [
		{
			'content_type'	: 'text',
			'title'			: msg.confirmation[lang],
			'payload'		: 'confirm'
		}
	] for lang in msg.languages
}
#####

#request_phone
request_phone = {
	lang : [
		{
			'content_type'	: 'user_phone_number',
			'title'			: msg.share_phone[lang],
		}
	] for lang in msg.languages
}
#####

#skip_avatar
skip_avatar = {
	lang : [ 
		{
			'content_type'	: 'text',
			'title'			: msg.skip_button[lang],
			'payload'		: 'skip'
		}
	] for lang in msg.languages
}
#####
