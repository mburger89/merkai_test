import json
import os
import sys
import time
import uuid 
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

test_results = {
    "test_id": "",
    "time_stamp": "",
    "tests": {
        "can_login": False,
        "device_count_equals_4": False,
        "device_detail_view_tests": {},
    }
}
sleep_time = 3

def get_result_not_equals(a, b):
    try:
        assert a != b
        return True
    except AssertionError:
        return False
    except Exception as error:
        print(error.with_traceback())

def write_results(results):
    with open(f"{os.getcwd()}/results/{results['test_id']}.json", "w") as file:
        json.dump(results, file)

def check_for_results_folder():
    if not os.path.exists(f'{os.getcwd()}/results'):
        os.mkdir(f'{os.getcwd()}/results')

def main(api_key):
    print("Test started")
    check_for_results_folder()
    test_run_res= test_results
    test_run_res["test_id"] = str(uuid.uuid4())
    test_run_res["time_stamp"] = str(datetime.now())
    driver = webdriver.Chrome()
    driver.get("https://meraki-web-test-v2.herokuapp.com")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "logo")))
    form_input =  driver.find_element((By.CSS_SELECTOR),"input[name=api_key]")
    form_input.send_keys(api_key)
    submit_button =  driver.find_element((By.CSS_SELECTOR), "input[type=submit]")
    submit_button.click()
    try :
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "devices")))
        test_run_res["tests"]["can_login"] = True
    except:
        print("Was not able to login with key given")
        write_results(test_run_res)
        print("Results write to json file in results folder")
        sys.exit(1)
    # Exit if we can not login with the provided key or auth takes longer than 30 seconds
    devices_url = driver.current_url
    devices_links = driver.find_elements((By.CSS_SELECTOR), 'div[class="devices"] a')
    test_run_res["tests"]["device_count_equals_4"] = True if len(devices_links) == 4 else False
    device_names = driver.find_elements((By.CSS_SELECTOR), "div[class='devices'] a > div[class=device] > div[class=details] p[class=name]")
    for i, device in enumerate(devices_links):
        device_name = device_names[i].text
        device.click()
        time.sleep(sleep_time)
        current_url = driver.current_url
        test_run_res["tests"]["device_detail_view_tests"][device_name] = {"page_changed" : get_result_not_equals(devices_url, current_url)}
        get_clients = driver.find_element((By.CSS_SELECTOR), "p span[class=clients]").text
        test_run_res["tests"]["device_detail_view_tests"][device_name].update({"client_count_not_empty": (len(get_clients) > 0)})
        driver.back()
    write_results(test_run_res)
    print("Results write to json file in results folder")
    driver.close()
    print("Test finished")

if __name__ == "__main__":
    args = sys.argv
    api_key = ""
    for i, arg in enumerate(args):
        if arg == "-key":
            api_key = args[i + 1]
    if api_key == "":
        print("Error: please provide api key with -key flag") 
        sys.exit(1)
   
    main(api_key)