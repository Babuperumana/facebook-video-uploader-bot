import messages as msg

language = [
	{
		"type"		: "postback",
		"title"		: lang,
		"payload"	: lang
	}
	for lang in msg.languages
]

#navigation
btn_home = {
	lang : {
		"type"		: "postback",
		"title"		: msg.home_button[lang],
		"payload"	: msg.home_button[lang]
		}
		for lang in msg.languages
}

btn_back = {
	lang : {
		"type"		: "postback",
		"title"		: msg.back_button[lang],
		"payload"	: msg.back_button[lang]
		}
		for lang in msg.languages
}

navigation = {
	lang : [ btn_home[lang], btn_back[lang] ]
		for lang in msg.languages
}
#####

#start
add_hotel_button = {
	lang :	{
		"type"		: "postback",
		"title"		: msg.add_place[lang],
		"payload"	: "add"
		}
		for lang in msg.languages
}
#####

#confirm
confirm_button = {
	lang : {
		"type"		: "postback",
		"title"		: msg.confirmation[lang],
		"payload"	: "confirm"
		}
		for lang in msg.languages
}
#####

#request_phone
request_phone = {
	lang : [
		{
		"type"		: "postback",
		"title"		: msg.share_phone[lang],
		"payload"	: "phone"
		},
		btn_home[lang], btn_back[lang]
		]
		for lang in msg.languages
}
#####

#skip_avatar
skip_button = {
	lang :	{
		"type"		: "postback",
		"title"		: msg.skip_button[lang],
		"payload"	: "skip"
		}
		for lang in msg.languages
}
#####
