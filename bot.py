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
type_nums = 0
type_operation = 0
type_time = 2


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
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Числа')
    itembtn2 = types.KeyboardButton('Операцию')
    itembtn3 = types.KeyboardButton('Время')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Определимся, что ты хочешь изменить..", reply_markup=markup)

@bot.message_handler(commands=['next'])
def send_next(message):
    if type_nums == 0:
        a = random.randint(10, 99)
        b = random.randint(10, 99)
    elif type_nums == 1:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
    elif type_nums == 2:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
    global res, type_operation
    if type_operation == 0:
        res = a+b
        bot.send_message(message.chat.id, "Сколько будет " + str(a) + " + " + str(b)+"?")
    elif type_operation == 1:
        res = a - b
        bot.send_message(message.chat.id, "Сколько будет " + str(a) + " - " + str(b) + "?")
    elif type_operation == 2:
        res = a * b
        bot.send_message(message.chat.id, "Сколько будет " + str(a) + " * " + str(b) + "?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    global answer
    try:
        answer = int(message.text)
    except ValueError:
        answer = 0
    if answer == 0:
        if str(message.text) == "Дальше!":
            send_next(message)
        elif str(message.text) == "Числа":
            markup = types.ReplyKeyboardMarkup(row_width=1)
            itembtn1 = types.KeyboardButton('Двухзначные')
            itembtn2 = types.KeyboardButton('Трехзначные')
            itembtn3 = types.KeyboardButton('Четырехзначные')
            itembtn4 = types.KeyboardButton('Настройки')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

            bot.send_message(message.chat.id, "Какие желаешь?", reply_markup=markup)
        elif str(message.text) == "Операцию":
            markup = types.ReplyKeyboardMarkup(row_width=1)
            itembtn1 = types.KeyboardButton('Сложение')
            itembtn2 = types.KeyboardButton('Вычитание')
            itembtn3 = types.KeyboardButton('Умножение')
            itembtn4 = types.KeyboardButton('Настройки')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

            bot.send_message(message.chat.id, "Что предпочитаешь?", reply_markup=markup)
        elif str(message.text) == "Время":
            markup = types.ReplyKeyboardMarkup(row_width=1)
            itembtn1 = types.KeyboardButton('5 секунд')
            itembtn2 = types.KeyboardButton('10 секунд')
            itembtn3 = types.KeyboardButton('20 секунд')
            itembtn4 = types.KeyboardButton('Настройки')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

            bot.send_message(message.chat.id, "Быстро считаешь?", reply_markup=markup)
        elif str(message.text) == "Настройки":
            send_settings(message)
        elif str(message.text) == "Стоп":
            send_welcome(message)
        else:
            global type_nums, type_operation, type_time
            if str(message.text) == "Двухзначные":
                type_nums = 0
            elif str(message.text) == "Трехзначные":
                type_nums = 1
            elif str(message.text) == "Четырехзначные":
                type_nums = 2
            elif str(message.text) == "Сложение":
                type_operation = 0
            elif str(message.text) == "Вычитание":
                type_operation = 1
            elif str(message.text) == "Умножение":
                type_operation = 2
            else:
                bot.send_message(message.chat.id, "Я такой команды не знаю..\n Узнай обо мне подробнее нажав /help")

    elif answer != 0:
        if answer == res:
            bot.send_message(message.chat.id, "Правильно! +1 очко Гриффиндору!")
        else:
            bot.send_message(message.chat.id, "Неа, правильный ответ " + str(res))
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Дальше!')
        itembtn2 = types.KeyboardButton('Стоп')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "Дальше?", reply_markup=markup)

bot.polling()