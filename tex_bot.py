import types

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import sqlite3
import os
import datetime as DT
import time
import json

# logfile = str(datetime.date.today()) + '.log' # формируем имя лог-файла
token = '5937676517:AAEG8U11wayyFFQmbJKi3Y3BdINCzUTIDWs'
admin_id = '734877274'
bot = telebot.TeleBot(token)
PHOTO_DIR = 'photo'
conn = sqlite3.connect('help_teh.db', check_same_thread=False)
markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """

global dish_dict
try :
    with conn :
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Programs")
        data = cursor.fetchall()  # fetchone
        column_names = [i[1] for i in conn.execute(f"SELECT * FROM Programs")]
        column_ids = [i[0] for i in conn.execute(f"SELECT * FROM Programs")]
        column_dict = dict(zip(column_names, column_ids))
except Exception as e :
    print(e)

try :
    with conn :
        data = conn.execute("SELECT * FROM Programs")
        prog_id = [str(i[0]) for i in conn.execute(f"SELECT * FROM Programs")]
        prog_name = [str(i[1]) for i in conn.execute(f"SELECT * FROM Programs")]

        prog_dict = dict(zip(prog_id, prog_name))
except Exception as e :
    print(e)

# Создаем клавиатуру и кнопки для главного меню USER-панели
Main_inline_keyb = InlineKeyboardMarkup()
Main_inline_keyb.add(InlineKeyboardButton("Регистрация", callback_data="menu:pushreg"))
Main_inline_keyb.add(InlineKeyboardButton("Список программ", callback_data="menu:txt1"))
Main_inline_keyb.add(InlineKeyboardButton("Мои коментарии", callback_data="menu:txt3"))
Main_inline_keyb.add(InlineKeyboardButton("О нас", callback_data="menu:txt2"))
Main_inline_keyb.add(InlineKeyboardButton("Профиль пользователя", callback_data="menu:profile"))
Main_inline_keyb.add(InlineKeyboardButton("Связь с оператором", callback_data="svyz:colling"))

# Создаем клавиатуру и кнопки для ADMIN-панели 1 уровня доступа
Admin_keyb_lvl1 = InlineKeyboardMarkup()
Admin_keyb_lvl1.add(InlineKeyboardButton("Добавить администратора➕", callback_data="admin_lvl1:addadmin"))
Admin_keyb_lvl1.add(InlineKeyboardButton("Удалить администратора➖", callback_data="admin_lvl1:deladmin"))
Admin_keyb_lvl1.add(InlineKeyboardButton("Редактировать профиль администратора🛠️", callback_data="admin_lvl1:redadmin"))

reviews_admin_keyb = InlineKeyboardMarkup()
reviews_admin_keyb.add((InlineKeyboardButton("Работа с отзывами", callback_data="admin:miniadmin")))
reviews_admin_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))

# Создаем клавиатуру и кнопки для ADMIN-панели 2 уровня доступа
Admin_keyb_lvl2 = InlineKeyboardMarkup()
Admin_keyb_lvl2.add(InlineKeyboardButton("Утвердить коментарий ", callback_data="admin_lvl2:admin_prog_rev"))
Admin_keyb_lvl2.add(InlineKeyboardButton("Добавить программу", callback_data="admin_lvl2:admin_prog_add"))

# """***START Функция для создания клавиатуры под карточкой программы START***"""
# def create_keyboard(prog_id):  # функция для создания клавиатуры под карточкой программы
#     markup_prog = InlineKeyboardMarkup(row_width=3)
#     markup_prog.add(InlineKeyboardButton('Описание', callback_data='prog_card:'),
#                     InlineKeyboardButton('+', callback_data='prog_card:plus'),
#                     InlineKeyboardButton("В корзину", callback_data="prog_card:basket"),
#                     InlineKeyboardButton('Коментарии', callback_data=f'prog_card:dish_feedback:{prog_id}'))
#     return markup_prog
# """***END Функция для создания клавиатуры под карточкой программы END***"""

#
"""***START Функция для создания клавиатуры для изменения профиля пользователя START***"""
profile_edit_data = {"Изменить имя" : "edit:name",
                     "Изменить телефон" : "edit:phone_number",
                     "Изменить адрес" : "edit:adress",
                     "Вернуться в меню" : "menu:b1"}


def create_edit_button(dct) :  # функция для создания кнопок для изменения полей профиля пользователя, принимает словарь
    edit_button = telebot.types.InlineKeyboardMarkup()
    for key, value in dct.items() :
        edit_button.add(telebot.types.InlineKeyboardButton(key, callback_data=value))
    return edit_button


"""***END Функция для создания клавиатуры для изменения профиля пользователя END***"""
#
global field, field_dict
field_dict = {"name" : "Имя", "phone_number" : "Телефон", "adress" : "Адрес"}
field = 'name'
global reg_name, reg_phone_number, reg_adress  # значения (данные юзера) при регистрации по умолчанию, к-е будем потом изменять
reg_name, reg_phone_number, reg_adress = "Указать имя", "Указать телефон", "Указать адрес"
global reg_field, reg_field_dict
reg_field = "name"  # получаем название поля для изменения
reg_field_dict = {"name" : "Имя", "phone_number" : "Телефон", "adress" : "Адрес"}


def create_registration_keyb() :  # функция для создания кнопок для регистрации пользователя
    registration_keyb = telebot.types.InlineKeyboardMarkup(row_width=1)
    registration_keyb.add(InlineKeyboardButton(reg_name, callback_data="reg:name"),
                          InlineKeyboardButton(reg_phone_number, callback_data="reg:phone_number"),
                          InlineKeyboardButton(reg_adress, callback_data="reg:adress"),

                          InlineKeyboardButton("Сохранить\u2705", callback_data="accept:save_all"),
                          InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
    return registration_keyb


# def create_admin_coment_keyb(dct):  # функция для создания клавиатуры для утверждения коментариев
#     AdminReviewProg_inline_keyb = InlineKeyboardMarkup(row_width=4)
#     AdminReviewProg_inline_keyb.add(InlineKeyboardButton("Номер", callback_data="qwerty:qwerty"),
#                                      InlineKeyboardButton("Статус", callback_data="qwerty:qwerty"),
#                                      InlineKeyboardButton("Утвердить", callback_data="qwerty:qwerty"),
#                                      InlineKeyboardButton("Отклонить", callback_data="qwerty:qwerty"))  # неактивные кнопки с фиктивным колбэком
#     for key, value in dct.items():
#         with conn:
#             current_coment_status = [i[4] for i in conn.execute(f"SELECT * FROM Programs WHERE id = {key}")][0]
#             print(current_coment_status)
#         AdminReviewProg_inline_keyb.add(InlineKeyboardButton(f"{key}.", callback_data=f"edit_coment:coment_{key}"),
#                                          InlineKeyboardButton(f"{value[2]}", callback_data="qwerty:qwerty"),
#                                          InlineKeyboardButton("\u2705", callback_data=f"+edit_coment:++{key}"),
#                                          InlineKeyboardButton("\u274C", callback_data=f"-edit_coment:--{key}"))
#     AdminReviewProg_inline_keyb.add(InlineKeyboardButton("Меню", callback_data="menu:b1"))
#     AdminReviewProg_inline_keyb.add(InlineKeyboardButton("Админка", callback_data="admin_lvl2:admin_panel"))
#     return AdminReviewProg_inline_keyb
#
global default_dict_add_prog
default_dict_add_prog = {1 : ["Добавить название", "Название", "Напишите название программы"],
                         2 : ["Добавить описание", "Описание", "Добавьте описание программы"],
                         3 : ["Добавить настройки", "Настройки", "Добавьте основные настройки"],
                         4 : ["Добавить инструкции", "Инструкции", "Укажите Инструкции для установки"],
                         5 : ["Добавить коментарии", "Коментарии", "Добавьте коментарии о программе"]}


def create_admin_addprog_keyb(dct) :  # функция для создания клавиатуры для добавления программы в БД, принимает словарь
    AdminAddProg_inline_keyb = InlineKeyboardMarkup(row_width=2)
    AdminAddProg_inline_keyb.add(InlineKeyboardButton("Выбрать:", callback_data="qwerty:qwerty"),
                                 InlineKeyboardButton("Результат:",
                                                      callback_data="qwerty:qwerty"))  # неактивные кнопки с фиктивным колбэком
    for key, value in dct.items() :
        AdminAddProg_inline_keyb.add(
            InlineKeyboardButton(f"{key}. {value[0]}", callback_data=f"admin_add_new_prog:add_prog_{key}"),
            InlineKeyboardButton(f"{value[1]}", callback_data="qwerty:qwerty"))
    AdminAddProg_inline_keyb.add(InlineKeyboardButton("Сохранить", callback_data="admin_add_dish:save_new_prog"))
    AdminAddProg_inline_keyb.add(InlineKeyboardButton("Админка", callback_data="admin_lvl2:admin_panel"))
    AdminAddProg_inline_keyb.add(InlineKeyboardButton("Меню", callback_data="menu:b1"))
    return AdminAddProg_inline_keyb


# оператор обратной связи
# def send_to_admin(message) :
#     bot.send_message(chat_id=admin_id, text=message)


#
# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#
#     user_message = message.text
#     send_to_admin(f'Пользователь {message.chat.id} написал: {user_message}')
#     bot.send_message(chat_id=message.chat.id, text='Спасибо за сообщение!')
#     if user_message == "stop":
#         bot.send_message(reply_markup=Main_inline_keyb)


@bot.message_handler(commands=['start'])
def start(message) :
    bot.send_message(message.chat.id, '''Привет! Я бот для технической поддержки пользователей программного обеспечения.
    \nДля начала работы пожалуйста пройдите регистрацию''', reply_markup=Main_inline_keyb)
    global user_telegram_id
    user_telegram_id = message.from_user.id
    print(user_telegram_id)


@bot.message_handler(commands=['addadmin'])
def add_admin(message) :
    user_id = message.from_user.id  # id телеги пользователя
    with conn :
        row = [i[1] for i in conn.execute("SELECT * FROM Admins WHERE position = 'admin lvl1'")]
    if user_id not in row :  # проверяем id на пригодность
        bot.send_message(message.chat.id, "Ошибка.\nНет правд доступа.", reply_markup=Main_inline_keyb)
    else :  # если есть, то показываем админу клаву для управления админкой
        bot.send_message(message.chat.id,
                         "Админ-панель 1 уровня.\n"
                         "Функционал: добавление, изменение и удаление админов 2 уровня.", reply_markup=Admin_keyb_lvl1)


@bot.message_handler(commands=['admin'])
def admin_management(message) :
    admin_id = message.from_user.id  # id телеги админа 2 уровня
    with conn :
        row = [i[1] for i in
               conn.execute("SELECT * FROM Admins WHERE position = 'admin lvl2' OR position = 'admin lvl1'")]
    if admin_id not in row :  # проверяем id
        bot.send_message(message.chat.id, "Ошибка.\nНет правд доступа.", reply_markup=Main_inline_keyb)
    else :  # если есть, то показываем админу клаву для управления админкой
        bot.send_message(message.chat.id,
                         "Админ-панель 2 уровня.\n"
                         "Функционал:\n"
                         "- Добавление и удаление программы;\n"
                         "- Обработка коментариев.", reply_markup=Admin_keyb_lvl2)


@bot.callback_query_handler(func=lambda call : call.data.split(":"))
def query_handler(call) :
    bot.answer_callback_query(callback_query_id=call.id)
    if call.data.split(':')[1] == "qwerty" :  # неактивные кнопки в админке
        print("qwerty")
    if call.data.split(':')[1] == "txt1" :
        print("список программ")
        global Proga_inline_keyb
        Proga_inline_keyb = InlineKeyboardMarkup()  # создаём кнопки списка программ
        [Proga_inline_keyb.add(InlineKeyboardButton(key, callback_data=f"{key}:{value}")) for key, value in
         column_dict.items()]
        Proga_inline_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
        bot.edit_message_text("Выберите программу: ", call.message.chat.id, call.message.message_id,
                              reply_markup=Proga_inline_keyb)
    if call.data.split(':')[1] == "b1" :
        bot.edit_message_text("Что Вас интересует?", call.message.chat.id, call.message.message_id,
                              reply_markup=Main_inline_keyb)
    if call.data.split(':')[1] == "b2" :
        bot.edit_message_text("Выберите программу", call.message.chat.id, call.message.message_id,
                              reply_markup=Proga_inline_keyb)
    if call.data.split(':')[0] in column_dict :
        print("программы")
        print(call.data.split(':')[0], call.data.split(':')[1])
        # Создаем клавиатуру и кнопки для программ
        global Sub_inline_keyb
        Sub_inline_keyb = InlineKeyboardMarkup()
        [Sub_inline_keyb.add(InlineKeyboardButton(key, callback_data=f"{key}:{value}")) for key, value in
         column_dict.items() if value == call.data.split(':')[1][1 :]]  # тут надо выкинуть карточку
        Sub_inline_keyb.add(InlineKeyboardButton("Особености работы программы", callback_data="info:work"))
        Sub_inline_keyb.add(InlineKeyboardButton("Установка и настройка", callback_data="info:sett"))
        Sub_inline_keyb.add(InlineKeyboardButton("Инструкции по использованию функций", callback_data="menu:b1"))
        Sub_inline_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
        Sub_inline_keyb.add(InlineKeyboardButton("Назад к выбору программ ", callback_data="menu:b2"))
        bot.edit_message_text("Чем я могу помочь?", call.message.chat.id, call.message.message_id,
                              reply_markup=Sub_inline_keyb)
    if call.data.split(':')[1] == "work" :
        cursor.execute(f"SELECT description From Programs")
        result = cursor.fetchone()
        print(result)
        global Desc_Inline_keyb
        Desc_Inline_keyb = InlineKeyboardMarkup()
        Desc_Inline_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
        Desc_Inline_keyb.add(InlineKeyboardButton("Назад к выбору программ ", callback_data="menu:b2"))
        # Desc_Inline_keyb.add(InlineKeyboardButton("Назад ",reply_markup= Sub_inline_keyb))
        bot.edit_message_text(result, call.message.chat.id, call.message.message_id, reply_markup=Desc_Inline_keyb)
    if call.data.split(':')[1] == "sett" :
        cursor.execute(f"SELECT settings From Programs")
        result = cursor.fetchone()
        print(result)
        global Sett_Inline_keyb
        Sett_Inline_keyb = InlineKeyboardMarkup()
        Sett_Inline_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
        Sett_Inline_keyb.add(InlineKeyboardButton("Назад к выбору программ ", callback_data="menu:b2"))
        bot.edit_message_text(result, call.message.chat.id, call.message.message_id, reply_markup=Sett_Inline_keyb)

    """___Обработка коллбэка от кнопки 'О нас'___"""
    if call.data.split(':')[1] == "txt2" :
        global Reviews_inline_keyb
        Reviews_inline_keyb = InlineKeyboardMarkup()
        Reviews_inline_keyb.add(InlineKeyboardButton("Отзывы о моей работе", callback_data="review:r1"))
        Reviews_inline_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
        about_restaurant = f"Добро пожаловать в чат-бот технической поддержки программного обеспечения! " \
                           f"Я готов помочь вам с любыми вопросами, связанными с работой программы." \
                           f" Я готов помочь вам с любыми вопросами, связанными с работой программы." \
                           f"  Если у вас возникнут какие-либо вопросы, не стесняйтесь обращаться ко мне. Я всегда готов помочь! "
        bot.edit_message_text(f"{about_restaurant}", call.message.chat.id, call.message.message_id,
                              parse_mode="Markdown", reply_markup=Reviews_inline_keyb)
    """""""""""""Регистрация"""""""""

    #     global field
    #     field = call.data.split(':')[1]
    # if call.data.split(':')[0] == "edit":
    #     bot.answer_callback_query(call.id)  # подтверждаем нажатие
    #     bot.send_message(call.message.chat.id, f"Введите новое значение для поля '{field_dict[field]}'.", reply_markup=telebot.types.ForceReply())\

    bot.answer_callback_query(call.id)
    user_id = call.from_user.id  # id телеги пользователя
    cursor.execute("SELECT * FROM Clients WHERE telegram_id = ?", (user_id,))  # проверка рег-ции пользователя в БД
    row = cursor.fetchone()
    if call.data.split(':')[1] == "pushreg" :
        Reg_inline_keyb = InlineKeyboardMarkup()
        Reg_inline_keyb.add(InlineKeyboardButton("РЕГИСТРАЦИЯ", callback_data="prereg:reg"))
        Reg_inline_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
        bot.edit_message_text("Чтобы пользоваться чат-ботом, нужно пройти регистрацию.", call.message.chat.id,
                              call.message.message_id,
                              reply_markup=Reg_inline_keyb)
    global reg_name, reg_phone_number, reg_adress  # значения регистрации по умолчанию
    if call.data.split(':')[1] == "reg" :
        with conn :
            conn.execute("INSERT OR IGNORE INTO Clients (name, phone_number, adress, telegram_id) values(?, ?, ?, ?)",
                         (reg_name, reg_phone_number, reg_adress, user_telegram_id))
        conn.commit()
        bot.answer_callback_query(call.id)  # подтверждаем нажатие
        bot.edit_message_text("Заполните все поля формы и сохраните данные:", call.message.chat.id,
                              call.message.message_id, reply_markup=create_registration_keyb())
    if call.data.split(':')[1] in reg_field_dict :
        global reg_field
        global Success_reg_inline_keyb
        reg_field = call.data.split(':')[1]
    if call.data.split(':')[0] == "reg" :
        bot.answer_callback_query(call.id)  # подтверждаем нажатие
        bot.send_message(call.message.chat.id, f"Введите значение для поля '{reg_field_dict[reg_field]}'.",
                         reply_markup=telebot.types.ForceReply())
    if call.data.split(':')[0] == "accept" :
        with conn :
            conn.execute("INSERT OR IGNORE INTO Clients (name, phone_number, adress, telegram_id) values(?, ?, ?, ?)",
                         (reg_name, reg_phone_number, reg_adress, user_telegram_id))
        conn.commit()
        print("Сохранено")
        bot.send_message(call.message.chat.id, f"Данные профиля успешно сохранены.", reply_markup=Main_inline_keyb)
    # if reg_name != "Указать имя" and reg_phone_number != "Указать телефон" and len(reg_phone_number) and reg_adress != "Указать адрес":
    #
    #     Success_reg_inline_keyb = InlineKeyboardMarkup()
    #     Success_reg_inline_keyb.add(InlineKeyboardButton("Вернуться в меню", callback_data="menu:b1"))
    #     bot.answer_callback_query(call.id)
    #     bot.send_message(call.message.chat.id, f"Вы успешно прошли регистрацию.\n"
    #                                            f"Ваш профиль:\n"
    #                                            f"Имя: {reg_name}\n"
    #                                            f"Телефон: {reg_phone_number}\n"
    #                                            f"Адрес: {reg_adress}\n\n"
    #                                            f"Вы можете изменить любое из этих полей в своём профиле.",
    #                      reply_markup=Success_reg_inline_keyb)

    # else:
    #     bot.send_message(call.message.chat.id, f"Введите корректные данные для всех полей и сохраните данные.", reply_markup=create_registration_keyb())

    """""""""""""АДМИНКАААААААААААА"""""""""""""
    if call.data.split(':')[1] == "addadmin" :
        add_inline_keyb = InlineKeyboardMarkup()
        add_inline_keyb.add(
            InlineKeyboardButton("Добавить данные о новом администраторе", callback_data="addm:adminid"))
        add_inline_keyb.add(InlineKeyboardButton("Вернуться назад↩ ", callback_data="addm:backmenu"))
        bot.send_message(call.message.chat.id, "Добавьте данные о новом администраторе", reply_markup=add_inline_keyb)
    if call.data.split(':')[1] == "backmenu" :
        bot.send_message(call.message.chat.id, "Добавьте данные о новом администраторе", reply_markup=Admin_keyb_lvl1)
    if call.data.split(":")[1] == "adminid" :
        bot.send_message(call.message.chat.id, "Введите telegram id нового администратора",
                         reply_markup=telebot.types.ForceReply())
    if call.data.split(':')[1] == "r1" :
        mini_admin_keyb = InlineKeyboardMarkup()
        mini_admin_keyb.add(
            InlineKeyboardButton("отзывы", callback_data="addm:reviews"))
        bot.edit_message_text("отзывы", call.message.chat.id, call.message.message_id, reply_markup=reviews_admin_keyb)
    # if call.data.split(":")[1] == "profile" :
    #     with conn :
    #         prof_name = [i[1] for i in conn.execute(f"SELECT * FROM Clients")]
    #         prof_phone_number = [i[2] for i in conn.execute(f"SELECT * FROM Clients")]
    #
    #         bot.send_message(call.message.chat.id, prof_name, prof_phone_number)


print("Ready")
bot.infinity_polling(none_stop=True, interval=0)
