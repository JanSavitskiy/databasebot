import sqlite3
import telebot

# Создание базы данных и таблицы
def create_database():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

# Добавление пользователя в базу данных
def add_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

# Инициализация бота
TOKEN = "YOUR_TOKEN"  # Замените на токен вашего бота
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    add_user(user_id)
    bot.send_message(message.chat.id, "Привет! Ваш ID сохранен в базе данных.")

@bot.message_handler(commands=['users_admin'])
def list_users(message):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()
    conn.close()

    if users:
        user_ids = "\n".join(str(user[0]) for user in users)
        bot.send_message(message.chat.id, f"Сохраненные ID пользователей:\n{user_ids}")
    else:
        bot.send_message(message.chat.id, "Нет сохраненных пользователей.")

def main():
    create_database()
    
    # Запуск бота
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
