import telebot
from datetime import datetime, timedelta, date
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8747369356:AAF590BuP60RFnwxzMs6b292d9g14N9Sa"

bot = telebot.TeleBot(TOKEN)

# Кнопки
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn_today = KeyboardButton("📅 СЕГОДНЯ")
btn_tomorrow = KeyboardButton("⏩ ЗАВТРА")
keyboard.add(btn_today, btn_tomorrow)

# База для определения чётности недели (20.04.2026 — ПН, 2-я неделя)
base_date = date(2026, 4, 20)

def get_week_parity():
    days_diff = (date.today() - base_date).days
    week_number = days_diff // 7
    return "even" if week_number % 2 == 0 else "odd"

def fmt(day, week):
    data = even_week.get(day) if week == "even" else odd_week.get(day)
    if not data:
        return f"📭 Расписания на {day} нет"
    week_name = "2-я неделя" if week == "even" else "1-я неделя"
    text = f"📅 **{day.upper()} ({week_name})**\n\n"
    for item in data:
        text += f"🕘 {item['time']}\n📚 {item['subject']} 🎓 ({item['type']})\n👨‍🏫 {item['teacher']} | 🏢 {item['place']}"
        if item.get('subgroup'):
            text += f" | {item['subgroup']} подгруппа"
        text += "\n\n"
    return text

# ========== 2-я НЕДЕЛЯ ==========
even_week = {
    "monday": [
        {"time": "08:00-09:30", "subject": "ЭКОЛОГИЯ", "type": "Лабораторная работа", "teacher": "Дичакова Л. С.", "place": "корп. C1 каб. 231", "subgroup": "1"},
        {"time": "09:40-11:10", "subject": "ЭКОЛОГИЯ", "type": "Лекция", "teacher": "Герасимова Л. А.", "place": "корп. C1 каб. 228", "subgroup": None},
        {"time": "11:30-13:00", "subject": "ЭКОЛОГИЯ", "type": "Лабораторная работа", "teacher": "Дичакова Л. С.", "place": "корп. C1 каб. 231", "subgroup": "2"},
        {"time": "13:30-15:00", "subject": "ФИЗИКА", "type": "Лабораторная работа", "teacher": "Мацынин А. А.", "place": "корп. А каб. 203", "subgroup": "1"},
        {"time": "15:10-16:40", "subject": "ФИЗИКА", "type": "Лабораторная работа", "teacher": "Мацынин А. А.", "place": "корп. А каб. 203", "subgroup": "2"}
    ],
    "tuesday": [
        {"time": "09:40-11:10", "subject": "ПРОФЕССИОНАЛЬНО-ПРИКЛАДНАЯ ФИЗИЧЕСКАЯ КУЛЬТУРА", "type": "Практика", "teacher": "Третьяков А. С.", "place": "корп. ДВС каб. Спортзал", "subgroup": None},
        {"time": "11:30-13:00", "subject": "МАТЕМАТИЧЕСКИЙ АНАЛИЗ", "type": "Лекция", "teacher": "Пашковская О. В.", "place": "корп. А каб. 204", "subgroup": None},
        {"time": "13:30-15:00", "subject": "МАТЕМАТИЧЕСКИЙ АНАЛИЗ", "type": "Практика", "teacher": "Пашковская О. В.", "place": "корп. А каб. 307", "subgroup": None},
        {"time": "15:10-16:40", "subject": "МАТЕМАТИЧЕСКИЙ АНАЛИЗ", "type": "Практика", "teacher": "Пашковская О. В.", "place": "корп. А каб. 307", "subgroup": None}
    ]
}

# ========== 1-я НЕДЕЛЯ ==========
odd_week = {
    "monday": [
        {"time": "08:00-09:30", "subject": "ИНОСТРАННЫЙ ЯЗЫК", "type": "Практика", "teacher": "Стрекалёва Т. В.", "place": "корп. Л каб. 906", "subgroup": "2"},
        {"time": "09:40-11:10", "subject": "ИНОСТРАННЫЙ ЯЗЫК", "type": "Практика", "teacher": "Стрекалёва Т. В.", "place": "корп. Л каб. 906", "subgroup": "2"},
        {"time": "11:30-13:00", "subject": "ФИЗИКА", "type": "Лекция", "teacher": "Мацынин А. А.", "place": "корп. А каб. 204", "subgroup": None},
        {"time": "13:30-15:00", "subject": "ИСТОРИЯ РОССИИ", "type": "Лекция", "teacher": "Сизых И. С.", "place": "корп. А каб. 204", "subgroup": None}
    ],
    "tuesday": [
        {"time": "09:40-11:10", "subject": "ПРОФЕССИОНАЛЬНО-ПРИКЛАДНАЯ ФИЗИЧЕСКАЯ КУЛЬТУРА", "type": "Практика", "teacher": "Третьяков А. С.", "place": "корп. ДВС каб. Спортзал", "subgroup": None},
        {"time": "11:30-13:00", "subject": "МАТЕМАТИЧЕСКИЙ АНАЛИЗ", "type": "Лекция", "teacher": "Пашковская О. В.", "place": "корп. А каб. 204", "subgroup": None},
        {"time": "13:30-15:00", "subject": "ИНОСТРАННЫЙ ЯЗЫК", "type": "Практика", "teacher": "Медников Д. М.", "place": "корп. Л каб. 911", "subgroup": "1"},
        {"time": "15:10-16:40", "subject": "ИНОСТРАННЫЙ ЯЗЫК", "type": "Практика", "teacher": "Медников Д. М.", "place": "корп. Л каб. 911", "subgroup": "1"}
    ]
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🎓 БНБ25-01 | СибГУ\n\n👇 Жми на кнопку:", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "📅 СЕГОДНЯ")
def today(m):
    day = datetime.now().strftime("%A").lower()
    week = get_week_parity()
    bot.send_message(m.chat.id, fmt(day, week), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "⏩ ЗАВТРА")
def tomorrow(m):
    day = (datetime.now() + timedelta(days=1)).strftime("%A").lower()
    week = get_week_parity()
    bot.send_message(m.chat.id, fmt(day, week), parse_mode="Markdown")

print("✅ Бот запущен")
bot.infinity_polling()
commit new file
