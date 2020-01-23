from config import admin_name

languages = {
	'ru'	: 'ru_RU',
	'en'	: 'en_US'
}
default_language = 'en'

#########
#messages
ask_language =	"Choose your language 🇬🇧\n"\
				"Выберите язык 🇷🇺"

about = {
	'ru' :	"Добавляйте места, в которых Вы останавливались во время Ваших поездок. "
			"Загружайте видео сторис об этих местах пребывания, чтобы другие "
			"путешественники могли составить реальную картину о достоинствах и недостатках "
			"каждого конкретного места проживания перед тем как их бронировать.",
	'en' :	"Add places you stayed at while traveling. "
			"Upload a video stories about your stays to help other travellers in figuring out "
			"the right places to stay on the basis of real stay experience before booking.",
}

greetings = {
	'ru' :	"*Приветствуем Вас в Stay Stories!* 🙌\n\n"\
			"У Вас есть видео 📹, которыми Вы хотите поделиться? 😉\n\n"\
			"Если возникли какие либо сложности или вопросы, напишите нам - {}"\
			"\n\nСменить язык - /language".format(admin_name),
	'en' :	"*Welcome to Stay Stories!* 🙌🏼\n\n"\
			"Upload your video stories 📹 and earn money 🤑🤑🤑\n\n"\
			"If any issues or questions arise, text us - {}"\
			"\n\nChange the language - /language".format(admin_name),
}
starting = {
	'ru' :	"Перед тем как загрузить свои видео, дайте знать *где и когда* они были сняты.\n"\
			"*Нажмите «Добавить место пребывания»*👇",
	'en' :	"Before you upload videos, let us know *where and when* these videos was shot.\n"\
			"*Press “Add a Place of Stay”*👇",
}
ask_again = {
	'ru' :	"Вы не добавили место пребывания.\n"\
			"*Нажмите «Добавить место пребывания»*👇",
	'en' :	"*Press “Add a Place of Stay”*👇",
}
ask_hotel = {
	'ru' :	"Укажите, где Вы останавливались.\n"\
			"Введите ссылку на страницу места проживания (booking.com или airbnb.com)",
	'en' :	"Paste a link to the property page (booking.com or airbnb.com)",
}
link_error = {
	'ru' :	"Упс! Такое ощущение, что эта ссылка не с booking.com или airbnb.com. Проверьте ссылку и попробуйте снова.",
	'en' :	"Ooops! It seems like the link is wrong. Check the link and try again.",
}
check_place = {
	'ru' :	"*Место пребывания:*\n{}, {}",
	'en' :	"*Place of stay:*\n{}, {}",
}
ask_date = {
	'ru' :	"В какие <strong>даты (примерно)</strong> Вы останавливались в этом месте?",
	'en' :	"<strong>When (approximately)</strong> did you stay at this place?",
}
later_date = {
	'ru' :	"Пожалуйста, выберите прошедшую дату",
	'en' :	"Please, select a past date",
}
conflict_date = {
	'ru' :	"Дата отъезда не может быть раньше даты заселения",
	'en' :	"Check out date can't be before check in",
}
check_date = {
	'ru' :	"*Даты пребывания:*\n{}",
	'en' :	"*Dates of stay:*\n{}"
}
ask_room_type =	{
	'ru' :	"Выберите тип комнаты, в которой Вы останавливались 👇",
	'en' :	"Choose a Room Type you stayed at:",
}
check_room = {
	'ru' :	"*Тип комнаты:*\n{}",
	'en' :	"*Room type:*\n{}"
}
ask_stay_type =	{
	'ru' :	"Выберите тип пребывания",
	'en' :	"Choose a Type of stay:",
}
check_stay = {
	'ru' :	"*Тип пребывания:*\n{}",
	'en' :	"*Type of stay:*\n{}"
}
ask_confirm = {
	'ru' :	"*Проверьте, перед тем как отправить видео:*\n",
	'en' :	"*Confirm before submit video*\n",
}
ask_video =	{
	'ru' :	"Нажмите на скрепочку, чтобы отправить видео",
	'en' :	"Press this button 📎 to choose and send a video",
}
not_a_video = {
	'ru' :	"Это не видео! Нажмите на скрепку, чтобы отправить видео",
	'en' :	"It seems like this is not a video. Press this button 📎 to choose and send a video",
}
video_thanks = {
	'ru' :	"Спасибо, Ваши Stay Stories загружены\n🔥💪😍",
	'en' :	"Thanks! Your Stay Stories has been uploaded",
}
ask_username = {
	'ru' :	"*Под каким аккаунтом* показывать Ваши видео в приложении Stay Stories?\n\n"\
			"Введите *никнейм* (латиницей)\nПример: bigboss",
	'en' :	"*Enter username* that will bee used to display your stories in the Stay Stories App.\n\n"\
			"e.g., bigboss",
}
wrong_username = {
	'ru' :	"Неверное имя аккаунта",
	'en' :	"Invalid username",
}
duplicate_username = {
	'ru' :	"Такой никнейм уже существует",
	'en' :	"This username already exists",
}
username_success = {
	'ru' :	"Аккаунт *{}* создан",
	'en' :	"Account *{}* has been created",
}
ask_phone =	{
	'ru' :	"Поделитесь *номером телефона* на который Вам будет отправлен проверочный код при заходе в приложение Stay Stories.\n\n"\
			"Нажмите *«Поделиться номером телефона»*",
	'en' :	"Share your *cell number* so you can get a code when log in to the Stay Stories App",
}
duplicate_phone = {
	'ru' :	"Пользователь с этим номером уже существует",
	'en' :	"Account with this phone already exists",
}
check_phone = {
	'ru' :	"*Номер телефона:*\n{}",
	'en' :	"*Phone number:*\n{}"
}
ask_avatar = {
	'ru' :	"Загрузите изображение для своего аккаунта, или нажмите «Пропустить»\n",
	'en' :	"Upload an image for the account (or press “Skip”)",
}
finish = {
	'ru' :	"Загрузите еще видео или нажмите *«Домой»*, чтобы добавить видео с нового места пребывания!",
	'en' :	"Upload more video or press “Home” button to add videos from another place of stay",
}
error_msg = {
	'ru' :	"Произошла ошибка. Попробуйте заново.",
	'en' :	"An error has occurred. Try again.",
}
conv_ended = {
	'ru' :	"Завершено",
	'en' :	"Conversation ended",
}

########
#buttons
home_button = {
	'ru' :	'🏠 Домой',
	'en' :	'🏠 Home',
}
back_button = {
	'ru' :	'⤴️ Вернуться',
	'en' :	'⤴️ Back',
}
pick_language = {
	'ru' :	'Русский',
	'en' :	'English',
}
add_place = {
	'ru' :	'Добавить место пребывания',
	'en' :	'Add a Place of Stay',
}
months = {
	'ru' :	['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
			'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
	'en' :	['January', 'February', 'March', 'April', 'May', 'June',
			'July', 'August', 'September', 'October', 'November', 'December'],
}
stays = {
	'ru' :	['Один', 'По работе', 'С семьёй', 'Парой', 'C друзьями'],
	'en' :	['Solo', 'On Business', 'With Family', 'Couple', 'With Friends']
}
confirmation = {
	'ru' :	'Подтвердить',
	'en' :	'Confirm',
}
share_phone = {
	'ru' :	'Поделиться номером телефона',
	'en' :	'Share phone number',
}
skip_button = {
	'ru' :	'Пропустить',
	'en' :	'Skip',
}

######
#admin
downloader_fail = (
	"Downloader module doesn't work, please, report to {0}"
	"\n\nЗагрузчик видео не работает, пожалуйста, сообщите {0}"
	.format(admin_name)
)
admin_options = [
	'Ввести код для загрузчика видео', 'Выслать новый код',
	'Выслать код на смс', 'Получить логи', 'Выход'
]
admin_msg = (
	"Если загрузчик не работает, в логах должно быть написано, почему (скорее всего, отвалилась авторизация)\n"
	"Не запрашивайте авторизацию слишком часто, телеграм отключит аккаунт на сутки"
)
