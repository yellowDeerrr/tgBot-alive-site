import telebot
from telebot import types
import functions
import threading

bot = telebot.TeleBot('7717982721:AAF0oulVplkeKM139_vmfsPMsizcqrpwnrQ')

# Keep track of the sending thread globally
sending_thread = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Start sending')
    markup.add(item1)
    bot.send_message(message.chat.id, "https://render-app-jtov.onrender.com", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    global sending_thread

    if message.text == 'Start sending':
        user_input_number = bot.send_message(message.chat.id, 'Enter minutes: ')
        bot.register_next_step_handler(user_input_number, set_minutes)

    elif message.text == 'Stop sending':
        if sending_thread and sending_thread.is_alive():
            functions.stop_sending()  # Signal the thread to stop
            bot.send_message(message.chat.id, "Sending process is stopping...")

            # Reset the buttons after stopping
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Start sending')
            markup.add(item1)
            bot.send_message(message.chat.id, "Choose", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Start sending')
            markup.add(item1)

            bot.send_message(message.chat.id, "No active sending process to stop.", reply_markup=markup)

def set_minutes(message):
    global sending_thread
    try:
        times_to_do_send = int(message.text) * 2  # Convert input to number of sends
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Stop sending')
        markup.add(button)
        bot.send_message(message.chat.id, "In process", reply_markup=markup)

        # Start the sending function in a new thread
        sending_thread = threading.Thread(target=functions.start_sending, args=(times_to_do_send, message, bot))
        sending_thread.start()  # Start the thread
        print("Started sending in a separate thread")
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number.")

if __name__ == "__main__":
    bot.infinity_polling()
