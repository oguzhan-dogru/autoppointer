# Author: Oguzhan Dogru
# Date 03 Feb 2024
# Reference: https://www.youtube.com/watch?v=SPM1tm2ZdK4

"""
Assumptions:
- no Captcha required
- no Login required
- we can infinitely refresh the webpage

Efficiency improvement:
- replace time.sleep with selenium wait
- shorten the loop
"""

import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def appointer():
    date_format = "%d.%m.%Y"  # Date dot month dot year  format
    counter = 1  # Initialize a counter for the while loop
    counter_max = 1000  # Stop re-trying after X attempts
    delay = 20  # Delay by X seconds not to flood the requests
    website = "https://www.google.com"  # The appointment portal

    # Initialize the browser
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    xpath = "xpath"
    driver.get(website)
    time.sleep(delay)

    # Find the element that contains date
    current_date = driver.find_elements(xpath,
                                        "//li[.//span[text()[contains(., 'Date:')]]]")

    date_old = current_date[0].text.split(' ')[-1]  # Extract the date 'dd.mm.yyyy' from a string
    date_old = datetime.strptime(date_old, date_format)  # Convert it to a numerical form (string2datetime_object)
    date_new = date_old + timedelta(days=1)  # Initialize a date to be compared. 'dd+1.mm.yyyy'

    # Find the button that says Reschedule
    reschedule_button = driver.find_elements(xpath,
                                             "//button[.//span[text()[contains(., 'Reschedule')]]]")
    reschedule_button[0].click()  # Click the reschedule button

    while (date_new >= date_old) and (
            counter < counter_max):  # If the counter didn't max, and the new date is not better
        next_button = driver.find_elements(xpath,
                                           "//button[.//span[text()[contains(., 'Next free appointments')]]]")
        next_button[0].click()  # Go to the next free appointments
        time.sleep(delay)

        Proposal_1 = driver.find_elements(xpath,
                                          "//tr[contains(@role, 'button')][.//th[text()[contains(., 'Proposal 1')]]]")

        date_new = Proposal_1[00].accessible_name.split(' ')[
            -2]  # Extract the date 'dd.mm.yyyy' of the best date in a list
        date_new = datetime.strptime(date_new, date_format)  # Convert it to a numerical form (string2datetime_object)

        if date_new < date_old:  # If this is a better date
            Proposal_1[00].click()  # Select it
            time.sleep(delay)

            confirm_button = driver.find_elements(xpath,
                                                  "//button[.//span[text()[contains(., 'Confirm rebooking')]]]")
            confirm_button[0].click()  # Confirm it
            driver.close()  # Terminate the browser window
            print('got it')
            break
        else:
            # Instead of refreshing the page, press a button that changes the view
            calendar_button = driver.find_elements(xpath,
                                                   "//button[.//span[text()[contains(., 'Show the calendar')]]]")
            calendar_button[0].click()  # reset
            time.sleep(delay)
            print('try again ', str(counter))

        counter += 1
        time.sleep(delay)


if __name__ == '__main__':
    appointer()
