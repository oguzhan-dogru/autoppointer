# Author: Oguzhan Dogru
# Date: 11 Feb 2024
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
    date_format = "%d.%m.%Y"  # Day dot month dot year format
    counter = 1  # Initialize a counter for the while loop
    counter_max = 1000  # Stop re-trying after X attempts
    delay = 20  # Delay by X seconds not to flood the requests
    website = "https://www.google.com"  # The appointment portal
    xpath = "xpath"

    # Initialize the browser
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(website)
    time.sleep(delay)

    # Find the element that contains date
    current_date = driver.find_elements(xpath, "//li[.//span[text()[contains(., 'Date:')]]]")
    # Extract the date 'dd.mm.yyyy' from a string and Convert it to a numerical form (string2datetime_object)
    date_old = datetime.strptime(current_date[0].text.split(' ')[-1], date_format)
    today = datetime.today()
    # Click the button that says Reschedule
    driver.find_elements(xpath, "//button[.//span[text()[contains(., 'Reschedule')]]]")[0].click()

    # If the counter didn't max out
    while counter < counter_max:
        # Go to the next free appointments
        driver.find_elements(xpath, "//button[.//span[text()[contains(., 'Next free appointments')]]]")[0].click()
        time.sleep(delay)

        proposal_1 = driver.find_elements(xpath,
                                          "//tr[contains(@role, 'button')][.//th[text()[contains(., 'Proposal 1')]]]")
        # Extract the date 'dd.mm.yyyy' of the lists best date and Convert it to string2datetime_object
        date_new = datetime.strptime(proposal_1[00].accessible_name.split(' ')[-2], date_format)

        # If this is a better date but not too early
        if (date_new < date_old) and (date_new >= today + timedelta(days=8)):
            proposal_1[00].click()  # Select it
            time.sleep(delay)
            # Confirm it
            driver.find_elements(xpath, "//button[.//span[text()[contains(., 'Confirm rebooking')]]]")[0].click()
            driver.close()  # Terminate the browser window
            print('got it ', date_new)
            break
        else:
            if date_new < today + timedelta(days=9):  # 9 instead of 8 to monitor the code's behaviour
                print('too early ')
            # Instead of refreshing the page, press a button that changes the view
            driver.find_elements(xpath, "//button[.//span[text()[contains(., 'Show the calendar')]]]")[0].click()
            time.sleep(delay)
            print(str(counter), 'try again ', date_new)

        counter += 1
        time.sleep(delay)


if __name__ == '__main__':

    restart_counter = 0
    max_restart_attempts = 5  # Set the maximum number of restart attempts

    while restart_counter < max_restart_attempts:
        try:
            appointer()
            break  # Break out of the loop if the script completes successfully
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(f"Restarting the script (attempt {restart_counter + 1}/{max_restart_attempts})...")
            restart_counter += 1

    if restart_counter == max_restart_attempts:
        print(f"Maximum restart attempts ({max_restart_attempts}) reached. Exiting.")
