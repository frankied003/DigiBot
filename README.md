# DigiBot
Beginner Shopify Bot

Base Folder - Sets up the selenium software to use throughout the code, such as shorcuts and it also
starts up the chrome driver instance.

Captcha Folder - This code is based on transferring the google recaptcha token using the sitekey,
domain name, and a local server ran on your computer. This is necessary to get passed captcha.

Json_files Folder - This code is simply where data is stored to be used throughout the entire code,
such as names, credit card info, keywords, different domain names, delays etc.

Pages - This is where all the action happens using selenium, beautiful soup, and many requests. There
are multiple pages for multible steps throughout the process of purchasing a sneaker, such as finding
the product, adding it to cart, then checking out. The names of the files aren't ideal.

Tests Folder - This is what file I run to run the entire code: new_test.py is the main file to run.

Utilities Folder - This is where all the logs and debugging happens to make speed up problem solving.

To Run:
1. Open the terminal and run as administrator
2. Navigate to the captcha folder
3. Type in: python server.py
4. The server should start
5. Navigate to the folder where the new_test.py file is
6. Type in: py.test -s -v new_test.py

To Modify:
1. Navigate to the json file called config.json
2. Edit with the info you want
