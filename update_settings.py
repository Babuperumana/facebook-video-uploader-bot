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
# 				"locale"	: locale,
# 				"text"		: msg.about[lang]
# 			} for lang, locale in msg.languages.items()
# 		] + [
# 			{
# 				"locale"	: "default",
# 				"text"		: msg.about[msg.default_language],
# 			}
# 		]
# 	)
# }

#############
# get started

# payload = {
# 	'get_started': json.dumps(
# 		{
# 			"payload"	: "/start"
# 		}
# 	)
# }

#################
#whitelist domain

payload = {
	"whitelisted_domains": json.dumps(
		[
			os.getenv('WEB_ADDRESS'),
		]
	)
}

url = "https://graph.facebook.com/v5.0/me/messenger_profile?access_token={}".format(os.getenv('ACCESS_TOKEN'))
responce = requests.post(url, payload)
print(responce.json())
