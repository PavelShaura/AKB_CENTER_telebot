import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

answer_list = []
answer_dict = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Какой у меня аккумулятор?', 'Показать адреса магазинов')
    msg = bot.send_message(message.chat.id,
                           " 👨🏻‍🔧 Добрый день! 👋🏻\n Я бот аккумуляторного центра.\n"
                           " Я могу помочь вам выбрать правильный аккумулятор для вашего автомобиля."
                           " Давайте начнем!",
                           reply_markup=markup
                           )
    bot.register_next_step_handler(msg, process_polarity_step)


def process_polarity_step(message):
    head = message.text
    if head == u'Какой у меня аккумулятор?':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Прямая', 'Обратная')
        msg = bot.send_message(message.chat.id,
                               " ❓ Для начала определим ПОЛЯРНОСТЬ вашего аккумулятора.\n"
                               " Полярность батареи - это направление положительной и отрицательной клемм."
                               " Положительная клемма помечена знаком ➕,"
                               " а отрицательная клемма  помечена знаком ➖."
                               " Прямая полярность означает, что положительная клемма находится слева,"
                               " а отрицательная - справа."
                               " Обратная полярность - наоборот. "
                               " Вот пример:",
                               reply_markup=markup)
        bot.send_photo(message.chat.id, open('image/polarity_example.png', 'rb'))
        bot.register_next_step_handler(msg, process_volume_step)

    elif head == u'Показать адреса магазинов':
        bot.send_message(message.chat.id, "г. Туапсе ул. Богдана Хмельницкого 106"
                                          " г. Туапсе ул. Фрунзе 61"
                                          " г. Туапсе ул. Жукова 9"
                         )


def process_volume_step(message):
    polarity = message.text
    answer_list.append(polarity)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("45 Ач", "55 Ач", "60 Ач", "66 Ач", "75 Ач", "77 Ач", "100 Ач", "140 Ач", "190 Ач", "200 Ач", )
    bot.send_message(message.chat.id, "✅ Отлично! \nТеперь мы знаем полярность!\n Двигаемся дальше!\n"
                                      " Теперь укажите примерный объем Вашего аккумулятора.")
    msg = bot.send_message(message.chat.id, "Объем батареи измеряется в Ач (ампер-часах). "
                                            "Наиболее распространенными объемами являются "
                                            " 45 Ач, 55 Ач, 60 Ач, 75 Ач и 100 Ач. "
                                            "Вот пример:",
                           reply_markup=markup
                           )
    bot.send_photo(message.chat.id, open('image/volume_example.jpg', 'rb'))
    bot.register_next_step_handler(msg, process_case_step)


def process_case_step(message):
    volume = message.text
    answer_list.append(volume)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("ЕВРОПЕЙСКИЙ", "АЗИАТСКИЙ")
    bot.send_message(message.chat.id, "✅ Отлично! \nТеперь мы знаем объем!\n Последний вопрос!\n"
                                      " Теперь укажите ТИП КОРПУСА АККУМУЛЯТОРА."
                     )
    msg = bot.send_message(message.chat.id,
                           "В АЗИАТСКИХ АКБ клеммы как бы торчат сверху, то есть возвышаются над ним. \n"
                           "В ЕВРОПЕЙСКОМ исполнении напротив, они утоплены и находятся как бы в нишах. \n"
                           "Вот пример:",
                           reply_markup=markup
                           )
    bot.send_photo(message.chat.id, open('image/case_example.jpg', 'rb'))
    bot.register_next_step_handler(msg, parse_data_answers)


def parse_data_answers(message):
    case_akb = message.text
    answer_list.append(case_akb)
    for key, answer in enumerate(answer_list, 1):
        answer_dict[key] = answer


bot.polling()
