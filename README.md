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