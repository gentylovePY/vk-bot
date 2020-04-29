import vk_api, random
import sqlite3
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
import schedule
import wikipedia
import requests


URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
Key = 'trnsl.1.1.20200211T173719Z.9fcd1fbfead36be4.04fdabdd2a3dd9891a5fa97e64c88d25a7080005'

vk_session = vk_api.VkApi(token="")"""You token public"""
wikipedia.set_lang("RU")
longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

conn = sqlite3.connect("db.db")  # конектимся к бд
c = conn.cursor()  # штукка помогающая испольнять бд наши команды

global Random


def random_id():
    Random = 0
    Random += random.randint(0, 1000000000);
    return Random


def check_if_exists(user_id):
    c.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    if result is None:
        return False
    return True


def register_new_user(user_id):
    c.execute("INSERT INTO users(user_id, state) VALUES (%d, ' ')" % user_id)
    conn.commit()
    c.execute("INSERT INTO user_info(user_id, user_wish) VALUES (%d, 0)" % user_id)
    conn.commit()

    c.execute("INSERT INTO play (user_id,balans) VALUES (%d,'0')" % user_id)
    conn.commit()


def get_user_state(user_id):
    c.execute("SELECT state FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def add_clas10a(user_id):
    c.execute("UPDATE users SET state= 10  WHERE user_id = %d" % user_id)
    conn.commit()


def add_clas10g(user_id):
    c.execute("UPDATE users SET state= 11 WHERE user_id = %d" % user_id)
    conn.commit()


def add_clas10e(user_id):
    c.execute("UPDATE users SET state= 12  WHERE user_id = %d" % user_id)
    conn.commit()


def lessons_10(lessons_10):
    if get_user_state(event.user_id) == 10:
        c.execute("SELECT lesson_%d FROM desatia " % lessons_10)
        result2 = c.fetchall()
        return result2[0][0]
    elif get_user_state(event.user_id) == 11:
        c.execute("SELECT lesson_%d FROM desatia " % lessons_10)
        result2 = c.fetchall()
        return result2[2][0]
    else:
        c.execute("SELECT lesson_%d FROM desatia " % lessons_10)
        result2 = c.fetchall()
        return result2[1][0]


def zvonki():
    c.execute("SELECT raspisaniezvonkov FROM raspisaniezvonkov  ")
    resul = c.fetchall()
    return resul[0][0]


def get_user_wish(user_id):
    c.execute("SELECT user_wish FROM user_info WHERE user_id = %d" % user_id)
    result = c.fetchone()
    return result[0]


def set_user_wish(user_id, user_wish):
    c.execute("UPDATE user_info SET user_wish = %d WHERE user_id = %d" % (user_wish, user_id))
    conn.commit()


def balans1(user_id):
    c.execute("SELECT balans FROM play   WHERE user_id = (%d)" % user_id)
    result89 = c.fetchone()
    return result89[0]





def play(user_id):


    c.execute("SELECT user_id FROM play   WHERE user_id = %d" % user_id)
    result88 = c.fetchone()
    return result88[0]



while True:



    for event in longpoll.check():


        if event.type == VkEventType.MESSAGE_NEW  and event.text and event.to_me :

            if not check_if_exists(event.user_id):
                register_new_user(event.user_id)

            if event.text.lower() == "начать":
                vk.messages.send(
                    user_id=event.user_id,
                    message="Привет!\nХочешь ли ты получать уведомления❓",
                    keyboard=open("uesorno.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )

            elif event.text.lower() == 'да❗':
                if get_user_wish(event.user_id) == 0:
                    set_user_wish(event.user_id, 1)
                vk.messages.send(
                    user_id=event.user_id,
                    message="Выбери свой класс👇🏻",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )
            elif event.text.lower() == 'нет🔕':

                vk.messages.send(
                    user_id=event.user_id,
                    message="Выбери свой класс👇🏻",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )

            elif event.text.lower() == 'расписание на завтра🔎':
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                tomorrow1 = tomorrow.weekday()
                vk.messages.send(
                    user_id=event.user_id,
                    message=lessons_10(tomorrow1),
                    keyboard=open('vonki.json', "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )



            elif event.text.lower() == 'назад⛔' or event.text.lower() == 'расписание':
                vk.messages.send(
                    user_id=event.user_id,
                    message="Выбери класс💢",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )

            elif event.text.lower() == "10-а":
                add_clas10a(event.user_id)
                vk.messages.send(
                    user_id=event.user_id,
                    message="Выбери, что тебе нужно❗",
                    keyboard=open("raspisanie.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )
            elif event.text.lower() == "расписание звонков⏱":
                vk.messages.send(
                    user_id=event.user_id,
                    message=zvonki(),
                    keyboard=open("raspisanie.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )

            elif event.text.lower() == "10-г":
                add_clas10g(event.user_id)
                vk.messages.send(
                    user_id=event.user_id,
                    message="Выбери, что тебе нужно❗",
                    keyboard=open("raspisanie.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )


            elif event.text.lower() == "10-е":
                add_clas10e(event.user_id)
                vk.messages.send(
                    user_id=event.user_id,
                    message="Выбери, что тебе нужно❗",
                    keyboard=open("raspisanie.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )
            elif event.text.lower() == 'переводчик' or  event.text.lower() == 'перевести еще что-нибудь' :

                vk.messages.send(
                    user_id=event.user_id,
                    message='какое слово нужно перевести?' ,
                    random_id=random_id()# Пишем "Введите запрос"
                )

                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                        if len(event.text)<=380:
                            def translate(text):
                                params = {
                                    "key": Key,
                                    "text": text,
                                    "lang": 'ru-en'
                                }
                                res = requests.get(URL, params=params)
                                return res.json()



                            json = translate(event.text)
                            print(''.join(json["text"]))
                            vk.messages.send(
                                user_id=event.user_id,
                                message=''.join(json["text"]),
                                keyboard=open('translate.json', "r", encoding="UTF-8").read(),
                                random_id=random_id()  # Пишем "Введите запрос"
                            )
                        else:
                            vk.messages.send(
                                user_id=event.user_id,
                                message='Текст слишком большой',
                                keyboard=open('translate.json', "r", encoding="UTF-8").read(),
                                random_id=random_id()  # Пишем "Введите запрос"
                            )
                        break

            elif event.text.lower() == 'играть' or event.text.lower() == 'сыграть еще раз' :

                vk.messages.send(
                    user_id=event.user_id,
                    message='Информация о игроке: \n ID Игрока = ' +str(play(event.user_id))+'\n Баланс игрока = '+str(balans1(event.user_id))+' р'+'\n\nИгра назавыется КОСТИ\nУ вас есть 4 попыток что бы сорвать кеш\nВыберите цыфру',
                    keyboard=open("cubik.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()  # Пишем "Введите запрос"
                )

                for number in range(4):
                    print('yf,th'+str(number))
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text :
                            print(event.text)
                            cube = random.randint(1,6)
                            user_win = random.randint(1000, 2500)
                            user_lose = random.randint(100, 500)
                            if event.text == str:
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Вы завершили игру\nДенег на счете= " + str(balans1(event.user_id)) + ' р',
                                    keyboard=open("end.json", "r", encoding="UTF-8").read(),
                                    random_id=random_id()
                                )
                                break
                                break

                            elif number == 3:

                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Вы завершили игру\nДенег на счете= " +str(balans1(event.user_id))+' р',
                                    keyboard=open("end.json", "r", encoding="UTF-8").read(),
                                    random_id=random_id()
                                )
                                break
                                break


                            elif event.text==cube:

                                win_balans=balans1(event.user_id)+user_win


                                print(win_balans)


                                def balans_win(win_balans,user_id):
                                    c.execute("UPDATE play SET balans=%d  WHERE user_id = %d" % (win_balans ,user_id))
                                    conn.commit()
                                balans_win(win_balans,event.user_id)
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Вы выйграли!!!\n\nКубик остановился на цифре: '+str(cube) +'\n Ваш ответ:'+event.text +'\n\nВаш выйграш составил '+  str(user_win)+' р',
                                    keyboard=open("cubik.json", "r", encoding="UTF-8").read(),
                                    random_id=random_id()  # Пишем "Введите запрос"
                                )



                            elif event.text!=cube:

                                lose_balans = balans1(event.user_id)-user_lose
                                def balans_lose(lose_balans,user_id):
                                    c.execute("UPDATE play SET balans=%d  WHERE user_id = %d" % (lose_balans,user_id))
                                    conn.commit()
                                balans_lose(lose_balans,event.user_id)

                                vk.messages.send(
                                    user_id=event.user_id,
                                    message='Вы не угадали(((\n\nКубик остановился на цифре:' + str(
                                        cube) + '\n Ваш ответ:' + event.text + '\n\n Вы проиграли ' + str(
                                        user_lose) + ' р',
                                    keyboard=open("cubik.json", "r", encoding="UTF-8").read(),
                                    random_id=random_id()  # Пишем "Введите запрос"
                                )


                                break
                                break





            else:
                vk.messages.send(
                    user_id=event.user_id,
                    message="Неизвестная команда",
                    keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                    random_id=random_id()
                )



