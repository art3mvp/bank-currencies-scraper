import re
import requests
import time
from selenium import webdriver
import json

currencies = {'R01239': 'EUR', 'R01235': 'USD','R01375': 'CNY'}

driver = webdriver.Chrome()

try:
    # Open the website
    driver.get("https://cbr.ru/")

    # time for page load and captcha pass 
    time.sleep(20)

    # Print XHR requests
    entries = driver.execute_script("return window.performance.getEntries();")
    xhr_entries = [i for i in entries if i.get('initiatorType') == 'xmlhttprequest']

    for xhr in xhr_entries:

        name_url = xhr.get('name') #'name': 'https://cbr.ru/cursonweek/?DT=&val_id=R01235&_=1704463087590'
        base_of_link, currency_url = name_url.split('?')

        attrs_pattern = re.compile(r'&|=')
        result = attrs_pattern.split(currency_url)
        attrs_dict = {result[i]: result[i + 1] for i in range(0, len(result), 2)} #{'DT': '', 'val_id': 'R01235', '_': '1704463087590'}

        if 'val_id' in attrs_dict:
            curr_name = currencies.get(attrs_dict['val_id'])
            data = {curr_name: requests.get(url=name_url).json()}
            

            with open(f'scraped_data_1.json', 'a') as file:
                json.dump(data, file, indent=2)

except Exception as e:
    print(f'Someting went wrong. Exception: {e}')
finally:
    driver.quit()
