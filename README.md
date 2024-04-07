# API_Automation

1) Create a virtual environment with : 

~~~
python -m venv env
~~~

- To activate the env, we must be stand in the env folder and use:

~~~
source Scripts/activate
(env) 
~~~

- To deactivate, run:
~~~
deactivate
~~~

2) install dependencies:

pytest 
requests
logging
python-dotenv


3) Add to the project the folders api, tests, utils

- Put inside utils folder the corresponding code for logger.py

- Put a folder for each endpoint under api folder

- Add an __init.py__ file on each folder

4) Test API endpoints:

- Messages endpoints:
  
  test_create_message has a particular definition, since the Mailsac API doesn´t suport email creation.

  An Office365 email credentials has been used to create a new email message, Mailsac code only confirm its received

  The code has a 30 seconds delay when you run it.

  python -m pytest test_messages.py