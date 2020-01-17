import requests
import os
import messages as msg
import json

###########
# greetings

# payload = {
# 	'greeting': json.dumps(
# 		[
# 			{
# 				"locale"	: "default",
# 				"text"		: msg.greetings['en'],
# 			},
# 			{
# 				"locale"	: "ru_RU",
# 				"text"		: msg.greetings['ru']
# 			},
# 		]
# 	)
# }

#############
# get started

payload = {
	'get_started': json.dumps(
		{
			"payload"	: "/start"
		}
	)
}

url = "https://graph.facebook.com/v5.0/me/messenger_profile?access_token={}".format(os.getenv('ACCESS_TOKEN'))
responce = requests.post(url, payload)
print(responce.json())
