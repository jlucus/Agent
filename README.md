# Virtual Casino VIP Host Release Notes 

## Version 1.1.0 June 30th, 2024 
## New Features 
- Interactive Inline Keyboard: Added inline keyboard buttons for user options such as "VIP Transfer", "Host/Concierge", and "Loss-back Availability".
- Additional Information Prompt: Users are now prompted with "Yes" or "No" buttons to include additional information for their host. 
- Automated Scheduling: Implemented a scheduling system that broadcasts messages to all authorized users at specific times of the day. 
## Improvements 
- User Data Management: Enhanced the system to store and manage user data and responses more efficiently. 
- Dynamic Message Handling: Improved the logic to dynamically handle user interactions based on their responses, providing a more personalized experience. 
## Fixes 
- Message Forwarding: Fixed an issue where user responses were not being forwarded to the correct group based on their casino choice. 
- Error Handling: Added better error handling for API exceptions, ensuring smoother operation and logging of issues. 
### Version 1.0.0 
### Initial Release 
- Basic Functionality: Initial release with basic bot functionality including user greeting, keyword recognition, and response handling. 
- User Interaction: Allowed users to select options and provide responses which were then forwarded to specific groups. 

# Installation 
1. Prerequisites: Python3, Virtual Enviornment, telebot, telebot.types InlineKeyboardMarkup InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, json, time, schedule, Thread, random. 
2. Begin by creating your project `mkdir agent` and then `cd agent`. 
3. Prepare your virtual enviorment using venv `pip install venv`. 
4. Install your required packages within your enviornment `.venv/bin/python -m pip install telebot`. 
5. Run the app by typing `python Agent.py` in your VSCode or other IDE terminal. 
6. Don't forget to define your `BOTTOKEN` and `GROUP_IDS` for your bot to forward appropriately.  
7. Enjoy.

# planned updates
## AI Agent Implementation - VIP Transfer Methodology:
🧙🏾‍♂️: Creating conversational AI agents within your bot, along with button prompts, involves a few key steps. We'll leverage the existing structure and add conversational capabilities. Here's an overview of how you can achieve this:

1. **Defining Conversational Flows**: Plan out the conversational paths that users can take. This includes the questions you want the bot to ask, the responses you expect, and the actions to be taken based on user input.
2. **Implementing Conversation Handlers**: Create functions to handle various stages of the conversation, ensuring smooth transitions and appropriate responses.
3. **Integrating Button Prompts**: Use inline buttons to guide users through the conversation, making it interactive and user-friendly.
4. **Natural Language Processing (NLP)**: Optionally, integrate NLP libraries like spaCy or NLTK for more advanced understanding of user inputs.

Let's focus on a practical implementation using your existing bot setup. We'll add a conversational flow for handling a "VIP Transfer" inquiry.

### Example: Conversational Flow for "VIP Transfer"

#### Step 1: Define the Conversational Flow
1. User selects "VIP Transfer" from the initial options.
2. Bot asks which casino the user is interested in.
3. User selects a casino.
4. Bot asks if the user wants to provide additional information.
5. User provides additional information or skips.
6. Bot confirms the details and forwards the message.

#### Step 2: Implement Conversation Handlers

```python
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
import json
import time
import schedule
from threading import Thread
import random

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(bot_token)

# List of greetings and prompts
greetings = ['Help with Gamba', 'Help with Shuffle', 'Help with Stake', 'Something else']

# File to store authorized users and responses
user_data_file = 'authorized_users.json'
responses_file = 'user_responses.json'

# Group IDs to forward messages to (replace with your actual group IDs)
group_ids = {
    'gamba': -1002192564730,
    'shuffle': -1002204969162,
    'stake': -1002191239622,
    'stake.us': -1002191239622,
    'other': -1002191239622
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
```
## This implementation allows the bot to handle conversational flows using button prompts, making the interaction more intuitive and user-friendly.
