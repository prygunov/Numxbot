import logging
import random
import time
from telebot import apihelper
import telebot
from telebot import types
apihelper.proxy = {'http':'http://142.93.251.123:8080'}
bot = telebot.TeleBot("749160827:AAEA1SDfQkEdn5t8-cV7VD9frHpxfdJ1rVo")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
res = 0
answer = 0



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

	bot.send_message(message.chat.id, "Привет, я просто бот, который поможет тебе научиться считать в уме, не используя калькулятор. \n\n "
						  "Вот команды которые ты можешь мне дать:\n"
				 "/help /start - вызовет вот это сообщение\n"
				 "/edit - изменить настройки\n"
				 "/next - задаст следующий пример")

@bot.message_handler(commands=['edit'])
def send_settings(message):

	bot.send_message(message.chat.id, "Кто сказал настройки?")
	time.sleep(3)
	markup = types.ReplyKeyboardMarkup(row_width=2)
	itembtn1 = types.KeyboardButton('Числа')
	itembtn2 = types.KeyboardButton('Операцию')
	itembtn3 = types.KeyboardButton('Время')
	markup.add(itembtn1, itembtn2, itembtn3)

	bot.send_message(message.chat.id, "Определимся, что ты хочешь изменить..", reply_markup=markup)

@bot.message_handler(commands=['next'])
def send_next(message):
	a = random.randint(2, 50)
	b = random.randint(2, 50)
	type = random.randint(0, 3)
	global res
	if type == 0:
		res = a+b
		bot.send_message(message.chat.id, "Сколько будет " + str(a) + " + " + str(b)+"?")
	elif type == 1:
		res = a - b
		bot.send_message(message.chat.id, "Сколько будет " + str(a) + " - " + str(b) + "?")
	elif type == 2:
		res = a * b
		bot.send_message(message.chat.id, "Сколько будет " + str(a) + " * " + str(b) + "?")
	elif type == 3:
		res = a // b
		bot.send_message(message.chat.id, "Сколько будет " + str(a) + " // " + str(b) + "?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	global answer
	try:
		answer = int(message.text)
	except ValueError:
		answer = 0
	if answer == 0:
		if str(message.text) == "Дальше!":
			print(1)
			send_next(message)
	elif answer != 0:
		if answer == res:
			bot.send_message(message.chat.id, "Правильно! +1 очко Гриффиндору!")
		else:
			bot.send_message(message.chat.id, "Неа, правильный ответ " + str(res))
		markup = types.ReplyKeyboardMarkup(row_width=1)
		itembtn1 = types.KeyboardButton('Дальше!')
		markup.add(itembtn1)
		bot.send_message(message.chat.id, "Дальше?", reply_markup=markup)
bot.polling()