import logging
from os import getenv

#bot
access_token	= getenv('ACCESS_TOKEN')
verify_token	= getenv('VERIFY_TOKEN')
log_name		= 'bot.log'
admin_name		= 'admin'

#api
api_prefix		= getenv('API_BRANCH')
api_get_user	= "https://{}.hotelstories.me/api/bot/getUser".format(api_prefix)
api_update_user	= "https://{}.hotelstories.me/api/bot/updateUser".format(api_prefix)
api_get_hotel	= "https://{}.hotelstories.me/api/bot/getHotel".format(api_prefix)
api_post_story	= "https://{}.hotelstories.me/api/bot/postVideo".format(api_prefix)

#aws
aws_kwargs = {
	'aws_access_key_id'		: getenv('AWS_ACCESS_KEY_ID'),
	'aws_secret_access_key'	: getenv('AWS_SECRET_ACCESS_KEY'),
	'region_name'			: getenv('AWS_DEFAULT_REGION'),
}
bucket_name = getenv('AWS_BUCKET')

#logger
logging.basicConfig(
	format		= '%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s',
	level		= logging.INFO,
	handlers	= [ logging.FileHandler(log_name), logging.StreamHandler() ],
)
