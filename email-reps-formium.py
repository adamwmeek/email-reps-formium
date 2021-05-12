"""
This script automates the contact form on Texas representatives' websites.
It will pull the data to use from txt files or prompt the user if the files are not present.
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import os

USER_FILE_NAME = 'user_info.txt'
ISSUE_FILE_NAME = 'HB_1399.txt'
CONTACT_URLS_NAME = 'contacts.txt'

prefix = ''
first_name = ''
last_name = ''
address = ''
city = ''
state = ''
zip_code = ''
email_address = ''

subject = ''
message = ''

if os.path.isfile(USER_FILE_NAME):

    with open(USER_FILE_NAME) as user_info_file:
        contents = user_info_file.readlines()

        prefix = contents[0].strip()
        first_name = contents[1].strip()
        last_name = contents[2].strip()
        address = contents[3].strip()
        city = contents[4].strip()
        state = contents[5].strip()
        zip_code = contents[6].strip()
        email_address = contents[7].strip()

else:

    prefix = input('Prefix? ')
    first_name = input('First name? ')
    last_name = input('Last Name? ')
    address = input('Address? ')
    city = input('City? ')
    state = input('State? ')
    zip_code = input('Zip code? ')
    email_address = input('Email address? ')

    with open(USER_FILE_NAME, 'w') as user_info_file:
        user_info_file.write(prefix + '\n')
        user_info_file.write(first_name + '\n')
        user_info_file.write(last_name + '\n')
        user_info_file.write(address + '\n')
        user_info_file.write(city + '\n')
        user_info_file.write(state + '\n')
        user_info_file.write(zip_code + '\n')
        user_info_file.write(email_address + '\n')

if os.path.isfile(ISSUE_FILE_NAME):

    with open(ISSUE_FILE_NAME) as issue_file:
        contents = issue_file.readlines()

        subject = contents[0].strip()
        message = contents[1:]

else:

    subject = input('Subject? ')
    message = input('Message? ')

    with open(ISSUE_FILE_NAME, 'w') as issue_file:
        issue_file.write(subject + '\n')
        issue_file.write(message)

with webdriver.Firefox() as browser:

    with open(CONTACT_URLS_NAME) as contact_urls_file:
        contents = contact_urls_file.readlines()

        for url in contents:

            browser.get(url)
            
            # Prefix
            prefix_select = Select(browser.find_element(By.NAME, 'prefix'))
            all_ops = [o.get_attribute('value') for o in prefix_select.options]
            prefix_select.select_by_value(prefix)
            
            # First name
            browser.find_element(By.NAME, 'name_first').send_keys(first_name)

            # Last name
            browser.find_element(By.NAME, 'name_last').send_keys(last_name)

            # Address
            browser.find_element(By.NAME, 'address').send_keys(address)

            # City
            browser.find_element(By.NAME, 'city').send_keys(city)

            # State
            browser.find_element(By.NAME, 'state').send_keys(state)

            # Zipcode
            browser.find_element(By.NAME, 'zip').send_keys(zip_code)

            # Email
            browser.find_element(By.NAME, 'email').send_keys(email_address)

            # Subject
            subjects = browser.find_elements(By.NAME, 'subject')
            subjects[1].send_keys(subject)

            # Message
            browser.find_element(By.NAME, 'message').send_keys(message)

            # pause to see what we've done so far...
            pause_action = ActionChains(browser)
            pause_action.pause(1)
            pause_action.perform()

            # Send the message 
            browser.find_element(By.NAME, 'Submit').click()