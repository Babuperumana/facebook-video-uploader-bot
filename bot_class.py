import os
from enum import Enum
import requests
from pymessenger import utils

DEFAULT_API_VERSION = 2.6

class NotificationType(Enum):
	regular = "REGULAR"
	silent_push = "SILENT_PUSH"
	no_push = "NO_PUSH"

class Bot:
	def __init__(self, access_token, **kwargs):
		"""
			@required:
				access_token
			@optional:
				api_version
				app_secret
		"""
		self.api_version = kwargs.get('api_version') or DEFAULT_API_VERSION
		self.app_secret = kwargs.get('app_secret')
		self.graph_url = 'https://graph.facebook.com/v{0}'.format(self.api_version)
		self.access_token = access_token

	@property
	def auth_args(self):
		if not hasattr(self, '_auth_args'):
			auth = {
				'access_token': self.access_token
			}
			if self.app_secret is not None:
				appsecret_proof = utils.generate_appsecret_proof(self.access_token, self.app_secret)
				auth['appsecret_proof'] = appsecret_proof
			self._auth_args = auth
		return self._auth_args

	def send_raw(self, payload):
		request_endpoint = '{0}/me/messages'.format(self.graph_url)
		response = requests.post(
			request_endpoint,
			params=self.auth_args,
			json=payload
		)
		result = response.json()
		return result

	def send_recipient(self, recipient_id, payload, notification_type=NotificationType.regular):
		payload['recipient'] = {
			'id': recipient_id
		}
		payload['notification_type'] = notification_type.value
		return self.send_raw(payload)

	def send_message(self, recipient_id, message, notification_type=NotificationType.regular):
		return self.send_recipient(recipient_id, {
			'message': message
		}, notification_type)

	def send_text_message(self, recipient_id, message, notification_type=NotificationType.regular):
		"""Send text messages to the specified recipient.
		https://developers.facebook.com/docs/messenger-platform/send-api-reference/text-message
		Input:
			recipient_id: recipient id to send to
			message: message to send
		Output:
			Response from API as <dict>
		"""
		return self.send_message(recipient_id, {
			'text': message
		}, notification_type)

	def send_generic_message(self, recipient_id, elements, notification_type=NotificationType.regular):
		"""Send generic messages to the specified recipient.
		https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template
		Input:
			recipient_id: recipient id to send to
			elements: generic message elements to send
		Output:
			Response from API as <dict>
		"""
		return self.send_message(recipient_id, {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": elements
				}
			}
		}, notification_type)

	def send_button_message(self, recipient_id, text, buttons, notification_type=NotificationType.regular):
		"""Send text messages to the specified recipient.
		https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template
		Input:
			recipient_id: recipient id to send to
			text: text of message to send
			buttons: buttons to send
		Output:
			Response from API as <dict>
		"""
		return self.send_message(recipient_id, {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "button",
					"text": text,
					"buttons": buttons
				}
			}
		}, notification_type)

	def send_quick_reply_message(self, recipient_id, text, buttons, notification_type=NotificationType.regular):
		return self.send_message(recipient_id, {
   			"text": text,
			"quick_replies": buttons
		}, notification_type)

	def send_action(self, recipient_id, action, notification_type=NotificationType.regular):
		"""Send typing indicators or send read receipts to the specified recipient.
		https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions

		Input:
			recipient_id: recipient id to send to
			action: action type (mark_seen, typing_on, typing_off)
		Output:
			Response from API as <dict>
		"""
		return self.send_recipient(recipient_id, {
			'sender_action': action
		}, notification_type)

	def get_user_info(self, recipient_id, fields=None):
		"""Getting information about the user
		https://developers.facebook.com/docs/messenger-platform/user-profile
		Input:
		  recipient_id: recipient id to send to
		Output:
		  Response from API as <dict>
		"""
		params = {}
		if fields is not None and isinstance(fields, (list, tuple)):
			params['fields'] = ",".join(fields)

		params.update(self.auth_args)

		request_endpoint = '{0}/{1}'.format(self.graph_url, recipient_id)
		response = requests.get(request_endpoint, params=params)
		if response.status_code == 200:
			return response.json()

		return None

	def send_webview_message(self, recipient_id, webview_type, ask_msg, button_msg, notification_type=NotificationType.regular):
		datepicker_url = (
			"{server_address}/{webview_type}?sender_id={sender_id}".format(
				server_address=os.getenv('WEB_ADDRESS'),
				webview_type=webview_type,
				sender_id=recipient_id
			)
		)
		return self.send_message(recipient_id, {
			"attachment" : { 
				"type"		: "template",
				"payload"	: {
					"template_type"	: "button",
					"text"			: ask_msg,
					"buttons"		: [{
						"type"					: "web_url",
						"url"					: datepicker_url, 
						"title"					: button_msg,
						"webview_height_ratio"	: "compact",
						"messenger_extensions"	: "true",
						"webview_share_button"	: "hide"
					}]
				}
			}
		}, notification_type)
