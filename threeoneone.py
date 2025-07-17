import random
import time
from datetime import datetime
from selenium.webdriver.common.by import By 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.chrome.options import Options
import logging

def safe_click(browser, element):
    try:
      element.click()
    except Exception as e:
       print(f"Selenium click failed with {e}, falling back to JS Click", flush=True)
       browser.execute_script("arguments[0].click();", element)
      
def run_selenium(user_location, complaint_reason, accessibility_input, route_num, route_dir, stop_id, incident_date_input, incident_time_input, first_name_input, last_name_input):
    #Browser Application setup
    #browser = webdriver.Chrome()
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("-width=1920")
    options.add_argument("-height=1080")
    #options.add_argument("--screenshot")

    browser = webdriver.Chrome(options=options)
    

    browser.get("https://windsor-cwiprod.motorolasolutions.com/cwi/tile")
    actions = ActionChains(browser)
    wait =  WebDriverWait(browser, 30)
    service_type_wait = wait.until(EC.visibility_of_element_located((By.XPATH, '//mat-label[contains(text(), "service")]/ancestor::mat-form-field//mat-select')))
    #Find and Select "Transit Windsor"
    service_type = browser.find_element(By.XPATH, '//mat-label[contains(text(), "service")]/ancestor::mat-form-field//mat-select')
    service_type.click()
    service_type_wait = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="mat-option-text" and normalize-space(text())="Transit Windsor"]')))
    service_type_field = browser.find_element(By.XPATH, '//span[@class="mat-option-text" and normalize-space(text())="Transit Windsor"]/ancestor::mat-option')
    service_type_field.send_keys(Keys.ENTER)
    print(" --- TRANSIT WINDSOR SELECTED ---", flush=True)
    actions.send_keys(Keys.TAB)

    #user_location = "Oulette Ave @ Park St E."
    location = browser.find_element(By.XPATH, '//input[contains(@data-placeholder, "Service Location")]')
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", location)
    #lwait = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[contains(@data-placeholder, "Service Location")]')))
    print(" --- LOCATION FOUND --- ", flush=True)
    time.sleep(1)
    safe_click(browser, location)
    location.send_keys(user_location)
    print(" --- LOCATION SENT --- ", flush=True)

    #Complaint
    call_reason = browser.find_element(By.XPATH, '//mat-label[contains(text(), "Call?")]/ancestor::mat-form-field//mat-select')
    actions.move_to_element(call_reason).perform()
    safe_click(browser, call_reason)
    browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", call_reason)
    time.sleep(0.5)
    call_reason = browser.find_element(By.XPATH, '//span[@class="mat-option-text" and normalize-space(text())="Complaint"]')
    safe_click(browser, call_reason)
    print(" --- COMPLAINT SELECTED --- ", flush=True) 
    #Its doing something weird so we need to click the body of the DOM to close the complaint window and "spawn" the "Reason for complaint"
    browser.find_element(By.XPATH, ("//body")).click() 
    print(" --- body selected --- ", flush=True)
    time.sleep(3)
    browser.get_screenshot_as_file("screenshots/screenshot.png") 
    #browser.get_screenshot_as_file("screenshots/screenshot.png")
    #Reason for Complaing
    
    complaint_reason_button = browser.find_element(By.XPATH,'//mat-label[contains(text(), "Complaint Type:")]/ancestor::mat-form-field//mat-select')
    try:
        actions.move_to_element(complaint_reason_button).perform()
    except Exception as e:
        print (f'Locating button failed with {e}, manually scrolling.')
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", complaint_reason_button)
        safe_click(browser, complaint_reason_button)
    
    #complain_wait = wait.until(EC.element_to_be_clickable((By.XPATH, '//mat-label[contains(text(), "Complaint Type:")]/ancestor::mat-form-field//mat-select')))
    time.sleep(1)
    complaint_reason = browser.find_element(By.XPATH, f'//span[@class="mat-option-text" and normalize-space(text())="{complaint_reason}"]')
    safe_click(browser, complaint_reason_button)
    actions.send_keys(Keys.ESCAPE)
    time.sleep(1)

    #Accessibility Issue
    accessibility_binary = browser.find_element(By.XPATH, '//mat-label[contains(text(), "accessibility")]/ancestor::mat-form-field//mat-select')
    actions.move_to_element(accessibility_binary).perform()
    #acc = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mat-option-44']/span")))
    safe_click(browser, accessibility_binary)
    #acc = WebDriverWait(browser,10).until(EC.presence_of_element_located(By.XPATH, "//*[@id='mat-option-44']/span"))

    time.sleep(1)
    if accessibility_input == "Yes":
        accessibility_binary = browser.find_element(By.XPATH, '//span[@class="mat-option-text" and normalize-space(text())="Yes"]')
        accessibility_binary.click()
        actions.send_keys(Keys.TAB)
    else:
        accessibility_binary = browser.find_element(By.XPATH, '//span[@class="mat-option-text" and normalize-space(text())="No"]')
        accessibility_binary.click()
        actions.send_keys(Keys.TAB)

    #Route Number
    route_number = browser.find_element(By.XPATH,'//mat-label[contains(text(), "Route Number")]/ancestor::mat-form-field//mat-select')
    actions.move_to_element(route_number).perform()
    rnumber_wait = wait.until(EC.element_to_be_clickable(route_number))
    print ("--- ROUTE NUMBER CLICKABLE ---", flush=True)
    safe_click(browser, route_number)
    route_number_xpath = f'//span[@class="mat-option-text" and normalize-space(text())="{route_num}"]'
    route_number = browser.find_element(By.XPATH,route_number_xpath)
    safe_click(browser, route_number)
    actions.send_keys(Keys.TAB)
    print ("--- ROUTE NUMBER SENT ---", flush=True)

    #Route Direction
    route_direction = browser.find_element(By.XPATH,'//mat-label[contains(text(), "Route Direction")]/ancestor::mat-form-field//mat-select')
    route_direction.click()
    route_direction_xpath = f'//span[@class="mat-option-text" and normalize-space(text())="{route_dir}"]'
    route_direction = browser.find_element(By.XPATH, route_direction_xpath)
    safe_click(browser, route_direction)
    actions.send_keys(Keys.TAB)
    print ("--- ROUTE DIRECTION SENT ---", flush=True)   

    #StopID
    stopID = browser.find_element(By.XPATH,'//textarea[contains(@aria-label, "Stop ID")]')
    actions.move_to_element(stopID)
    stopID_parent = browser.find_element(By.XPATH,'//textarea[contains(@aria-label, "Stop ID")]/ancestor::mat-form-field')
    print ("--- STOP ID FOUND ---", flush=True)  
    stopID.send_keys(stop_id)
    actions.send_keys(Keys.TAB)

    #Incident Date
    print("DATE: ", incident_date_input)
    #Because HTML formats dates YYYY/MM/DD but the city wants it MM/DD/YYYY we need to do some stuff
    #The date input will always be YYYY-MM-DD. 
    # We can use txt.split and the "-"" as the seperator
    x = incident_date_input.split("-")
    #Take the output array and reconfigure the indices from MM-DD-YYYY, then overwrite the input variable
    incident_date_input=f'{x[1]}-{x[2]}-{x[0]}'
    print(incident_date_input) #Check format
    incident_date = browser.find_element(By.XPATH, '//input[contains(@aria-label, "Date of incident")]') 
    actions.scroll_to_element(incident_date).perform()
    safe_click(browser, incident_date)
    
    incident_date.send_keys(incident_date_input) #Enter in reconfigured date
    actions.send_keys(Keys.TAB)

    #Incident Time
    incident_time = browser.find_element(By.XPATH, '//input[contains(@data-placeholder, "Time of incident")]')
    actions.scroll_by_amount(0,3).perform()
    
    incident_time.send_keys(incident_time_input)
    actions.send_keys(Keys.TAB)
    actions.send_keys(Keys.TAB)

    #Submit Name & Email
    first_name = browser.find_element(By.XPATH, '//input[contains(@data-placeholder, "First Name")]')
    actions.move_to_element(first_name).perform()
    first_name.send_keys(first_name_input)

    #Submit Name & Email
    last_name = browser.find_element(By.XPATH, '//input[contains(@data-placeholder, "Last Name")]')
    actions.move_to_element(last_name).perform()
    last_name.send_keys(last_name_input)

    time.sleep(5)
    print("Program Complete. The browser will close.", flush=True)

