import telebot
from telebot import types
import random
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)
conn = psycopg2.connect(host = "159.223.20.145", dbname = "server", password = "codabra", user = 'server')
db = conn.cursor()

@bot.message_handler(content_types=['text'])
def idle(message):
    if message.text == '/start' and checkuser(message.from_user.id) == False:
        bot.send_message(message.from_user.id, "Добро пожаловать в Дальноземье, назови своего персонажа")
        bot.register_next_step_handler(message, givename)
    if message.text == '/test':
        getstarts(message.from_user.id)
    if message.text == '/test2':
        getenemyes(message.from_user.id)



def givename(message):
    name = message.text
    db.execute("INSERT INTO persona (user_id, name) VALUES (%s, %s)", (message.from_user.id, name))
    conn.commit
    bot.send_message(message.from_user.id, "Привет " + name + ". Напиши команду /game.")


def checkuser(id):
    db.execute("SELECT * FROM persona WHERE user_id = %s", (id,))
    if db.fetchone() is None:
        return False
    else:
        return True

#0. id
#1. hp
#2. energy
#3. attack
#4. defend
#5. villagers
#6. steals
#7. name

def getstarts(id):
    db.execute("SELECT * FROM persona WHERE user_id = %s", (id,))
    answer = db.fetchone()
    bot.send_message(id,
f'''
привет'{answer[7]}'вот твоя статистика
здоровье -'{answer[1]}
енергия - {answer[2]}
урон - {answer[3]}
защита - {answer[4]}
последователи - {answer[5]}
стеалс - {answer[6]}''')

def getenemyes(id):
    db.execute("SELECT * FROM enemy")
    answer = db.fetchall()
    text = ''



    for enemy in answer:
        text += f'''
---
Имя - {enemy[5]}/ здоровье - {enemy[1]}/ урон - {enemy[2]}/ защита - {enemy[3]}/ зоркость - {enemy[4]}
---
'''
    bot.send_message(id, text)


bot.polling(none_stop=True, interval=0)