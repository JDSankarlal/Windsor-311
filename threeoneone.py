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
import logging



def run_selenium(user_location, complaint_reason, accessibility_input, route_num, route_dir, stop_id, incident_date_input, incident_time_input, first_name_input, last_name_input):
    #Browser Application setup
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("https://windsor-cwiprod.motorolasolutions.com/cwi/tile")
    actions = ActionChains(browser)
    time.sleep(1)
    #Find and Select "Transit Windsor"
    service_type = browser.find_element(By.XPATH, '//mat-label[contains(text(), "service")]/ancestor::mat-form-field//mat-select')
    service_type.click()
    service_type = browser.find_element(By.XPATH, "//*[@id='mat-option-35']/span")
    service_type.click()
    time.sleep(1)
    actions.send_keys(Keys.TAB)

    #user_location = "Oulette Ave @ Park St E."
    location = browser.find_element(By.ID, "mat-input-0")
    location.send_keys(user_location)
    time.sleep(1)


    #Complaint
    call_reason = browser.find_element(By.XPATH, '//mat-label[contains(text(), "Call?")]/ancestor::mat-form-field//mat-select')
    actions.move_to_element(call_reason).perform()
    call_reason.click()
    time.sleep(1)
    call_reason = browser.find_element(By.XPATH, '//span[@class="mat-option-text" and normalize-space(text())="Complaint"]')
    call_reason.click()
    
    #Its doing something weird so we need to click the body of the DOM to close the complaint window and "spawn" the "Reason for complaint"
    browser.find_element(By.XPATH, ("//body")).click()
    #Do a big scroll
    scroll_origin = ScrollOrigin.from_element(location,0,-50)
    actions.scroll_from_origin(scroll_origin,0,400)\
    .perform()

    wait =  WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, '//mat-label[contains(text(), "Complaint Type:")]/ancestor::mat-form-field//mat-select')))
    
    #Reason for Complaing
    complaint_reason_button = browser.find_element(By.XPATH,'//mat-label[contains(text(), "Complaint Type:")]/ancestor::mat-form-field//mat-select')
    actions.move_to_element(complaint_reason_button).perform()
    complaint_reason_button.click()
    time.sleep(1)
    complaint_reason = browser.find_element(By.XPATH, f'//span[@class="mat-option-text" and normalize-space(text())="{complaint_reason}"]')
    complaint_reason.click()
    actions.send_keys(Keys.ESCAPE)
    time.sleep

    #Accessibility Issue
    accessibility_binary = browser.find_element(By.XPATH, '//mat-label[contains(text(), "accessibility")]/ancestor::mat-form-field//mat-select')
    actions.move_to_element(accessibility_binary).perform()
    #acc = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mat-option-44']/span")))
    accessibility_binary.click()
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
    route_number = browser.find_element(By.ID, "mat-select-8")
    route_number.click()
    route_number_xpath = f'//span[@class="mat-option-text" and normalize-space(text())="{route_num}"]'
    route_number = browser.find_element(By.XPATH,route_number_xpath)
    route_number.click()
    actions.send_keys(Keys.TAB)

    #Route Direction
    route_direction = browser.find_element(By.ID, "mat-select-value-11")
    route_direction.click()
    route_direction_xpath = f'//span[@class="mat-option-text" and normalize-space(text())="{route_dir}"]'
    route_direction = browser.find_element(By.XPATH, route_direction_xpath)
    route_direction.click()
    actions.send_keys(Keys.TAB)   

    #StopID
    stopID = browser.find_element(By.ID, "mat-input-2")
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
    incident_date.click()
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
    first_name.send_keys(last_name_input)

    time.sleep(5)
    print("Program Complete. The browser will close.")

