# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = 'BOT_TOKEN_HERE'
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
import json
import time
import schedule
from threading import Thread
import random

bot = telebot.TeleBot(bot_token)

# List of keywords to look for
keywords = ['vip transfer', 'host/concierge', 'loss-back availability']

# List of greetings and prompts
greeting_keywords = ['hi', 'start', 'help', 'agent']
greetings = ['Help with Gamba', 'Help with Shuffle', 'Help with Stake', 'Something else']
suggestions = ["lossback", "VIP", "vip", "host", "help"]

# File to store authorized users and responses
user_data_file = 'authorized_users.json'
responses_file = 'user_responses.json'

# Group IDs to forward messages to (replace with your actual group IDs)
group_ids = {
    'gamba': GAMBAGROUPID,   # Replace with actual group ID for Gamba
    'shuffle': SHUFFLEGROUPID, # Replace with actual group ID for Shuffle
    'stake': STAKEGROUPID,   # Replace with actual group ID for Stake
    'stake.us': STAKEUSGROUPID, # Replace with actual group ID for Stake.US
    'other': OTHERGROUPID    # Replace with actual group ID for other inquiries
}

# Load authorized users
def load_users():
    try:
        with open(user_data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save authorized users
def save_users(users):
    with open(user_data_file, 'w') as file:
        json.dump(users, file, indent=4)

# Load user responses
def load_responses():
    try:
        with open(responses_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user responses
def save_responses(responses):
    with open(responses_file, 'w') as file:
        json.dump(responses, file, indent=4)

# Initialize user data and responses
user_data = load_users()
user_responses = load_responses()

# Function to create an inline keyboard with options
def create_inline_keyboard(options):
    keyboard = InlineKeyboardMarkup()
    for option in options:
        button = InlineKeyboardButton(text=option.capitalize(), callback_data=option)
        keyboard.add(button)
    return keyboard

# Function to create a keyboard with greeting options
def create_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for greeting in greetings:
        button = KeyboardButton(greeting)
        keyboard.add(button)
    return keyboard

# Handle the /start command or a greeting message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or str(user_id)
    
    # Save user if not already saved
    if str(user_id) not in user_data:
        user_data[str(user_id)] = username
        save_users(user_data)
        print(f"New user saved: {username} (ID: {user_id})")

    # Greet the user and ask how the bot can help
    greeting = random.choice(greetings)
    response_message = f"{greeting} How can I assist you today?"
    options = ['VIP Transfer', 'Host/Concierge', 'Loss-back Availability']
    bot.send_message(message.chat.id, response_message, reply_markup=create_inline_keyboard(options))
    print(f"Greeting sent to {username} (ID: {user_id}).")

# Handle button presses
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call: CallbackQuery):
    message = call.message
    user_id = message.chat.id
    callback_data = call.data.lower()
    
    if str(user_id) not in user_responses:
        user_responses[str(user_id)] = []
    
    user_responses[str(user_id)].append(callback_data)
    save_responses(user_responses)

    # Check the stage of the interaction
    if callback_data in ['vip transfer', 'host/concierge', 'loss-back availability']:
        if callback_data == 'vip transfer':
            response_message = "Great! We can help you with your VIP transfer. Which casino are you interested in?"
        elif callback_data == 'host/concierge':
            response_message = "We are happy to notify your host. Which casino are you interested in?"
        elif callback_data == 'loss-back availability':
            response_message = "Sorry about your recent luck, but we can look into it for you. Which casino is this about?"

        options = ['Gamba', 'Shuffle', 'Stake', 'Stake.us', 'Other']
        bot.edit_message_text(response_message, chat_id=message.chat.id, message_id=message.message_id, reply_markup=create_inline_keyboard(options))
        print(f"Prompting {user_id} for casino selection.")

    elif callback_data in ['gamba', 'shuffle', 'stake', 'stake.us', 'other']:
        response_message = "Would you like to include any additional information for your host?"
        options = ['Yes', 'No']
        bot.edit_message_text(response_message, chat_id=message.chat.id, message_id=message.message_id, reply_markup=create_inline_keyboard(options))
        print(f"Asking {user_id} if they want to include additional information.")

    elif callback_data == 'yes':
        bot.send_message(message.chat.id, "Please provide the additional information.")
        bot.register_next_step_handler(message, handle_additional_info)
        print(f"Prompting {user_id} for additional information.")

    elif callback_data == 'no':
        user_response_text = '\n'.join(user_responses.get(str(user_id), [])[-5:])
        final_message = f"Thank you for your input! Your host has been notified. Good luck!\n\n" \
                        f"Here are your most recent responses:\n{user_response_text}"
        bot.edit_message_text(final_message, chat_id=message.chat.id, message_id=message.message_id)
        print(f"Host notification message sent to {user_id}.")

        # Determine the group ID to forward to
        casino_choice = user_responses.get(str(user_id))[-2]  # Second last response is the casino choice
        group_id = group_ids.get(casino_choice, group_ids['other'])
        
        # Forward the response to the appropriate group
        try:
            bot.send_message(group_id, f"User {user_id} (ID: {user_id}) provided the following details:\n\n{user_response_text}")
            print(f"Forwarded user details to {casino_choice} group (ID: {group_id}).")
        except telebot.apihelper.ApiException as e:
            print(f"An error occurred: {e}")

def handle_additional_info(message):
    user_id = message.chat.id
    additional_info = message.text
    group_id = group_ids.get(user_responses.get(str(user_id))[-2], group_ids['other'])

    bot.send_message(group_id, f"User {user_id} (ID: {user_id}) provided the following additional information:\n\n{additional_info}")
    bot.send_message(message.chat.id, "Your information has been forwarded to the group.")
    print(f"Forwarded additional information from {user_id} to group (ID: {group_id}).")

# Function to broadcast a message to all authorized users
def broadcast_message():
    for user_id in user_data:
        try:
            bot.send_message(user_id, "This is a scheduled broadcast message. Please check for updates!")
            print(f"Broadcast message sent to {user_data[user_id]} (ID: {user_id}).")
        except telebot.apihelper.ApiException as e:
            print(f"An error occurred while sending to {user_data[user_id]}: {e}")

# Function to schedule broadcasts
def schedule_broadcasts():
    schedule.every().day.at("09:00").do(broadcast_message)
    schedule.every().day.at("12:00").do(broadcast_message)
    schedule.every().day.at("18:00").do(broadcast_message)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduling thread
def start_scheduler():
    scheduler_thread = Thread(target=schedule_broadcasts)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# Start polling for new messages
def start_polling():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Start the scheduler
    start_scheduler()

    # Start polling
    start_polling()