from lxml import html
from os import getenv
import requests

def booking(url):

	info = {}
	url = requests.get(url).url.split('?')[0].split('#')[0]
	info['link'] = requests.get(url + '?lang=en-us').url.split('?')[0]
	doc = html.fromstring(requests.get(info['link']).content)

	name = doc.xpath("//h2[@id='hp_hotel_name']/text()[2]")[0]
	address = doc.xpath("//span[contains(@class, 'hp_address_subtitle')]/text()")[0]
	rooms = doc.xpath("//a[@class='jqrt togglelink']/@data-room-name-en")
	id_booking = doc.xpath("//div[@class='hp-lists js-hp-wl-sidebar hide']/@data-hotel-id")[0]
	coords = doc.xpath("//a[@id='hotel_address']/@data-atlas-latlng")[0].split(',')

	info['id']			= id_booking
	info['name']		= name.strip()
	info['latitude']	= coords[0]
	info['longitude']	= coords[1]
	info['address']	= address.strip()
	address = info['address'].split(',')
	info['country']	= address[-1].strip()
	info['city']	= address[-2].strip()
	info['rooms'] = []
	for room in rooms:
		info['rooms'].append(room.strip())
	if not info['rooms']:
		info['rooms'].append("Standard Room")
	return info

airbnb_params = {
	"key"		: getenv('AIRBNB_API_KEY'),
	"_format"	: "for_rooms_show"
}

def airbnb(url):
	if 'me' in url:
		url = requests.get(url).url	
	info = {}
	info['id'] = url.split('/')[-1].split('?')[0]
	request_url = "https://www.airbnb.com/api/v2/pdp_listing_details/" + info['id']
	response = requests.get(request_url, params=airbnb_params)
	js = response.json()['pdp_listing_detail']
	info['name']		= js['name']
	info['latitude']	= js['lat']
	info['longitude']	= js['lng']
	info['address']		= js['p3_summary_address']
	address = info['address'].split(',')
	info['country']	= address[-1].strip()
	info['city']	= address[-2].strip()
	info['link']	= js['seo_features']['og_tags']['og_url']
	info['rooms']	= [ js['p3_event_data_logging']['room_type'] ]
	return info

def parseUrl(url):
	if not url:
		raise Exception('No link found')
	if url[:7] != 'http://' and url[:8] != 'https://':
		url = 'https://' + url
	if "booking." in url:
		hotel_data = booking(url)
		hotel_data['site'] = 'booking'
	elif "airbnb." in url:
		hotel_data = airbnb(url)
		hotel_data['site'] = 'airbnb'
	else:
		raise Exception('Wrong site')
	if hotel_data.keys() < {'id', 'name', 'address'}:
		raise Exception('Not enough info got')
	return hotel_data
