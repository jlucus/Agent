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
**Installing a virtual environment for Python 3 using a Bash terminal (common in Unix-like systems such as Linux and macOS) is a straightforward process.** 

## Step 1: Install Python 3
**Make sure Python 3 is installed on your system. You can install it using a package manager or download it from the official Python website.**

>_ For Ubuntu/Debian-based systems: _

`bash`  
`sudo apt update`  
`sudo apt install python3 python3-pip`  

**For macOS using Homebrew:**

`bash`  
`brew install python3`  

## Step 2: Verify Installation
**Check that Python 3 and pip3 (the Python package installer for Python 3) are installed:**

`bash`  
`python3 --version`  
**OR**  
`pip3 --version`  
**Both commands should return the version numbers.**  
  
## Step 3: Install virtualenv Package  
**Install the virtualenv package using pip3:**  
`bash`  
`pip3 install virtualenv`  

## Step 4: Create a Project Directory   
**Navigate to or create the directory where you want to set up your project:**  
  
`bash`  
`mkdir my_project`  
`cd my_project`  
Replace `my_project` with your desired project directory name.  
   
## Step 5: Create a Virtual Environment  
**Create a virtual environment in your project directory. Replace env with your preferred environment name:**  

`bash`  
`python3 -m venv env`  
**This creates a virtual environment named env in your current directory.**  
  
## Step 6: Activate the Virtual Environment  
**Activate the virtual environment. The activation script is located in the bin directory within your virtual environment:**  
  
`bash`  

`source env/bin/activate`  
**Once activated, your prompt will change to show that you are now working within the virtual environment (usually the environment name will appear in parentheses).**  
  
## Step 7: Install Required Packages  
**With the virtual environment activated, you can install any necessary packages using pip (no need to specify pip3 inside the environment):**  
  
`bash`  
  
`pip install package_name`  
**To list all installed packages:**  
  
`bash`  
`pip list`  
