import random
import time
from datetime import datetime
from tkinter import *
from tkcalendar import Calendar
from tkcalendar import DateEntry
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

# ###Form###
# root = Tk()
# root.title("Transit 311 Report")
# root.columnconfigure(0, weight=1)
# root.columnconfigure(1, weight=1)

# location_label = Label(root, text = "Intersection or Location")
# location_label.grid(column=0,row=1)
# location_labelField = Entry()
# location_labelField.grid(column=1, row =1)

# acc_label= Label(root, text = "Is this an accessibility issue impacting a person with a disability?")
# acc_label.grid(column=0, row=2)

# acc_var = IntVar()
# radio_button_y = Radiobutton(root, text="Yes",padx=20, variable=acc_var, value=1)
# radio_button_n = Radiobutton(root, text="No",padx=20, variable=acc_var, value=0)
# radio_button_y.grid(column=1,row=2)
# radio_button_n.grid(column=2,row=2)

# route_label = Label(root, text = "Select Route")
# route_label.grid(column=0, row = 4)
# route_list = [
#     " ",
#     "115",
#     "305",
#     "418X",
#     "518X",
#     "605 (Amherstburg)",
#     "Central 3",
#     "Crosstown 2",
#     "Dougall 6",
#     "25 (LaSalle)",
#     "Lauzon 10",
#     "LTW 42 (Leamington to Windsor)",
#     "Ottawa 4",
#     "Parent 14",
#     "South Windsor 7",
#     "Transway 1A",
#     "Transway 1C",
#     "Walkerville 8",
#     "School Extra",
#     "Special Events",
#     "Tunnel Bus",
#     "Not Known"
# ]
# route_value = StringVar(root)
# route_value.set("Bus Route Number (if known)")
# route_menu = OptionMenu (root, route_value, *route_list)
# route_menu.grid(column=1, row=4, columnspan=2, sticky=W+E)

# route_dir_label = Label(root, text = "Select Route Direction")
# route_dir_label.grid(column=0, row = 5)
# route_dir_list = [
#     "Northbound",
#     "Southbound",
#     "Eastbound",
#     "Westbound",
# ]
# route_dir_value = StringVar(root)
# route_dir_value.set("Bus Route Direction")
# route_dir_menu = OptionMenu(root, route_dir_value, *route_dir_list)
# route_dir_menu.grid(column=1, row = 5, columnspan=2, sticky = W+E)


# stopid_label = Label(root, text = "Stop ID")
# stopid_label.grid(column=0,row=12)
# stopid_labelField = Entry()
# stopid_labelField.grid(column=1, row =12)


# cal_label = Label (root, text = "Date of Incident: ")
# cal_label.grid(column=0, row=13)
# cal = Calendar(root, selectmode = 'day', year = 2025, month = 7, day = 11, date_pattern = 'MM/dd/yyyy')
# #The 311 website requires yyyy, so we change the DateEntry format here to send to the website later! 
# cal.grid(column = 1, row = 13)

# time_label = Label (root, text = "Input time of Incident: ")
# time_label.grid(column=0, row = 15)

# timeHr_label = Label(root, text = "Hour")
# timeHr_label.grid(column = 1, row = 14)
# timeHr_field = Entry()
# timeHr_field.grid(column = 1, row = 15)

# timeMin_label = Label(root, text = "Minute")
# timeMin_label.grid(column=2, row = 14)
# timeMin_field = Entry()
# timeMin_field.grid (column = 2, row = 15)

# timeAM_label = Label (root, text = "AM/PM")
# timeAM_label.grid(column = 2, row = 14)

# time_list = ["AM","PM"]
# timeAM_value = StringVar(root)
# timeAM_value.set("AM")
# timeAM_field = OptionMenu(root,timeAM_value, *time_list)
# timeAM_field.grid(column= 4, row = 15)


# def get_report_data():
#     tk_user_location = location_labelField.get()
#     tk_accessibility_input = acc_var.get()
#     tk_route_num = route_value.get()
#     tk_stop_id = stopid_labelField.get()
#     tk_route_dir = route_dir_value.get()
#     tk_date = cal.get_date()
#     tk_hour = timeHr_field.get()
#     tk_minute = timeMin_field.get()
#     tk_amPM = timeAM_value.get()
    
#     user_location = tk_user_location
#     accessibility_input = tk_accessibility_input
#     route_num = tk_route_num
#     stop_id = tk_stop_id
#     route_dir = tk_route_dir
#     incident_date_input = tk_date
#     incident_time_input = str(tk_hour) + str(tk_minute) + tk_amPM 
#     run_selenium(user_location, accessibility_input, route_num, route_dir, stop_id, incident_date_input, incident_time_input)


# submit_button = Button (root, text="Submit", command = get_report_data)
# submit_button.grid(column = 0, row = 20)

# root.mainloop()

# ##################

