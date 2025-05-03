from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Замените на свой токен, полученный от @BotFather
TOKEN = '7818440005:AAEnaIS5ep2NP0KG2GRzNBjI2ejtN5Pq5ng'
# Замените на свой Telegram ID (узнать можно через @userinfobot)
ADMIN_ID = '7413915232'

def escape_markdown_v2(text):
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

# Приветственное сообщение для новых участников
WELCOME_MESSAGE = (
    "Напишите Заказ:\n"
    "(услуги как на примере: 1,2,3,6,8)\n"
    "(ваш текст)"
)

# Обработка новых участников
def handle_new_member(update, context):
    if update.message.new_chat_members:  # Проверяем, есть ли новые участники
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:  # Если добавили самого бота
                update.message.reply_text("Добавьте меня в группу, и я начну работать!")
            else:  # Если добавили нового участника
                update.message.reply_text(WELCOME_MESSAGE)

# Обработка заказов
def handle_order(update, context):
    print("Проверка обработки заказа...")
    if update.message.chat.type in ['group', 'supergroup'] and update.message.text.lower().startswith("заказ:"):
        print("Условие 'заказ:' выполнено")
        user = update.message.from_user
        if user.username:
            user_link = f"@{user.username}"  # @username не требует экранирования
        else:
            user_name = escape_markdown_v2(user.first_name)
            user_link = f"[{user_name}](tg://user?id={user.id})"
        
        order_text = escape_markdown_v2(update.message.text)
        print(f"Пользователь: {user_link}, Текст заказа: {order_text}")
        
        # Отправляем пользователю подтверждение
        update.message.reply_text("Ваш заказ принят! Ожидайте ответа.(для оплаты пройдите в телеграм-бота: @batarei_mynouit_bot)")
        
        # Формируем сообщение для администратора с экранированием
        admin_message = f"Новый заказ от {user_link}:\n{order_text}"
        print(f"Сообщение для администратора: {admin_message}")
        
        # Пытаемся отправить сообщение администратору
        try:
            context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode='MarkdownV2')
            print("Сообщение успешно отправлено администратору")
        except Exception as e:
            print(f"Ошибка при отправке сообщения администратору: {e}")
            # Пробуем отправить без форматирования, если MarkdownV2 не работает
            try:
                context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
                print("Сообщение отправлено администратору без форматирования")
            except Exception as e:
                print(f"Ошибка при отправке без форматирования: {e}")

# Основная функция
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчики
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, handle_new_member))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_order))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
