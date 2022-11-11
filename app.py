from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from details import username, password  # Linkedin password and username Stored in details.py file
import pyautogui



url_Career = "https://www.careerguide.com/career-options"   # career Guide website for the Job name 
url = "https://www.linkedin.com/login"  # linkedin Login page url


driver = webdriver.Firefox()     # Im using FireFox you can use Chrome driver if u need  
driver.maximize_window()          # to Maximize the Window    


# To Open the Career Guide Website 
def Open():
    count = 0            # I used Count to Screen out most of the data For the Test You can disable it
    title = []       # All the Job names Are Stored In this List
    driver.get(url_Career)          #open the Link
    sleep(3)
    # Below line is used to find the div tag containing all the Job in their Respective fild we only take the text present on the Website page and not thir Whole data
    values = driver.find_element(By.XPATH, '/html/body/form/div[6]/div[3]/div/div[2]').text     
    # print(values)
    values = values.splitlines()    # The values we got are in line format to remove the \n metacharacter we use this
    
    # For Loop to traverse all the data/text present in the values retrived from the page
    for x in values:
        title.append(x)
        # if you want to get all the Job titles then remove the three lines below 
        # I kept This to stop my Pc from Overheating and crashing
        count +=1
        if count == 2:
            break 
    print(title)
    Open_Browser(title)     # Moving to the linkedin Page 
    
    
def Open_Browser(titleL):       # Linkedin Page Scraping 
    driver.get(url)
    driver.implicitly_wait(5)
    sleep(3)
    #  Below line are to locate the username and password input field based on their ID and enter the data
    login_block = driver.find_element(By.ID, 'username')
    login_block.send_keys(username)
    password_block = driver.find_element(By.ID, 'password')
    password_block.send_keys(password)
    password_block.send_keys(Keys.ENTER)
    sleep(2)
    pyautogui.confirm(text='Press Ok After Clearing the Captcha', title='Security Check Control', buttons=['OK'])       # To Wait until The user enters the captcha and Press OK the Programm will not Execute Further.
    sleep(2)
    
    for i in range(len(titleL)):        # To Search for the job For all the listed Job Title present in Title list
        #  these three variables are reset So that it can store data related to Other Job Titles
        Job_details = []        # Contains Job Position, company, Place
        application_link = []       # Contais all the link Locations
        company = []                # Contains the Link to the Company Linkedin Page
        print(f"\t{titleL[i]} details -->")
        sleep(4)
        driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3350373647&geoId=100811329&keywords={}&location=Karnataka%2C%20India&refresh=true'.format(titleL[i]))    # Open the Link for the Job title Search 
        sleep(2)
        
        ul_body = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')     # Selecting the Container/Box Containg all the Jobs Listed for the Search Title
        items = ul_body.find_elements(By.TAG_NAME, 'li')    # Selecting only the list tags inside the container
        
        # Searching all the li tags (list tags) for the data present in them about the Job 
        for item in items:
            text = item.text        # Job details of li tag only scraps for the text displayed on the website without worrying about the inner data
            text = text.splitlines()
            # to avoid Empty and Single lists We screen them based on the list size An Normal List would have 7 attributes Found on the Website Job Card
            if len(text) > 4:
                Job_details.append(text)
        print(f"\tJob details for {titleL[i]}-->\t {Job_details}")

        items = ul_body.find_elements(By.TAG_NAME, 'a')     # Check for all the 'a' tags present in the Container 
        
        # Search for all the 'a' tag for Links associated with it.
        for item in items:
            all_links = item.get_attribute('href')      # We Only take the href part from the 'a' tag
            # to Seperate The Company Linkedin Links and Push them into the Company Link List 
            if ".com/company/" in all_links:
                company.append(all_links)
            # To sepearte The Job Application Link and add Them to the Job application link list
            elif ".com/jobs/view/" in all_links:
                #To Filter the Dublication of the Link from The a tags present in the Company Icon
                if all_links not in application_link:
                    application_link.append(all_links)
        print(f"\tThe Link For The Application for {titleL[i]}\t {application_link}")
        print(f"\tCompany linkedin Page Link--> {company}\t")
        print(f"\tThe company Details Link For {titleL[i]}\t")
        # Add the Page to open the Company Details Link And Scrap the Necessary Detail

        for i in range(len(company)):
            About_dict = {}
            driver.get(company[i])          # TO Open The Company Linkedin Profile Page Stored in the Company list
            sleep(2)
            
            # Searching For the About Button And Opening The About Page of The Respective Company
            aboutBtn = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[1]/section/footer')
            aboutBtn.click()
            sleep(2)
            
            # Searching for the Description Box of the Company and Adding it to the Dictionary
            detail_box = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/p').text
            About_dict['description'] = detail_box
            sleep(2)
            
            # Searching For the Number Of Employees Currently Working for them and Adding it To the Dictionary
            Employee_box = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[3]').text
            # print(Employee_box)
            About_dict['no Employees'] = Employee_box
            sleep(2)
            
            # Searching for the Comapny Headquater Location And Adding it to the Dictionary
            Comp_Location = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div/div[1]/section/dl/dd[5]').text
            # print(Comp_Location)
            About_dict["headquater"] = Comp_Location
            sleep(2)
            
            print(f'The Company Details --->{About_dict}')
            sleep(3)
        
        
        print("\n")


Open()
# login()
sleep(2)
