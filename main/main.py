import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
from datetime import date
from urllib.parse import unquote, quote
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import track
import csv 


myoptions = Options()
myoptions.headless = True  # Run in headless mode for faster performance

# Create a Firefox profile object
profile = webdriver.FirefoxProfile()

# Set preferences to disable image loading
profile.set_preference("permissions.default.image", 2)

# Attach the profile to options
myoptions.profile = profile

myoptions.add_argument('--disable-extensions')  # Disable extensions
myoptions.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
myoptions.add_argument('--no-sandbox')  # Bypass OS security model
myoptions.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
myoptions.add_argument('--disable-logging')  # Disable logging
console = Console()

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
spider = '''
                                     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠶⡄⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                    ⠀⠀⠀⠀⠀⠀⠀⢀⣤⠤⣤⡀⢀⡗⠒⣧⠴⠋⠚⠉⠙⠳⣄⠀⠀⠀⠀⠀⠀⠀
                                    ⠀⠀⠀⠀⠀⠀⢀⡞⢁⣠⡟⠻⣎⠃⢰⠏⠀⠀⠀⠀⠀⠀⢘⣧⣤⣄⡀⠀⠀⠀
                                    ⠀⠀⠀⠀⠀⣠⠞⠓⡶⢦⣻⡄⣨⠷⠚⠒⠶⡤⠀⠀⢀⡴⠋⠁⢠⣇⠙⢳⣄⠀
                                    ⠀⠀⠀⢠⣞⠁⣠⠶⢧⣄⠈⣿⠳⠶⢤⣀⠀⠈⢩⠴⠟⠛⣯⠙⢳⡌⠻⣯⡘⡆
                                    ⠀⠀⢠⠏⢈⡟⠁⢀⣠⣤⠖⣿⡤⣄⣀⠙⢧⣀⣸⡀⠘⣦⡛⢳⡴⠻⣄⠈⠉⠁
                                    ⢀⣴⠟⢳⡞⢀⡴⠋⠀⣼⠗⡿⢠⡏⢹⣇⣤⡽⢫⡉⢻⡁⢹⡄⠻⣄⣸⠧⣄⡀
                                    ⠘⠶⠖⠋⣠⠟⢙⡶⢺⠷⣴⠛⠺⢦⡾⠐⣾⣇⣼⡇⠀⣟⠋⢷⠀⠈⠳⢤⡤⠇
                                    ⠀⠀⠀⣴⠛⣦⠏⠀⣼⣀⡏⠀⠀⣼⠦⣾⠉⡇⠸⠇⠀⢹⣀⣸⡆⠀⠀⠀⠀⠀
                                    ⠀⠀⡼⢧⣴⠃⠀⢸⣃⡼⠁⠀⠀⣿⣤⣿⠀⡟⠉⣇⠀⠀⢿⡀⢻⡀⠀⠀⠀⠀
                                    ⠀⠸⣇⡼⠃⠀⠀⠀⠉⠀⠀⠀⠀⠹⣤⡿⠀⢿⣠⣿⠀⠀⠀⠙⠋⠀⠀⠀⠀⠀
                                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                                                                                                                  
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓██████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓██████▓▒░   
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓██████▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓████████▓▒░ 
                                                                                                                     
  _  _                   _  _                                  _   _  _                  __      __                _ 
 | \| |_____ _____ _ _  | || |_  _ _ _ _ _ _  _   __ _ _ _  __| | | \| |_____ _____ _ _  \ \    / /__ _ _ _ _ _  _| |
 | .` / -_) V / -_) '_| | __ | || | '_| '_| || | / _` | ' \/ _` | | .` / -_) V / -_) '_|  \ \/\/ / _ \ '_| '_| || |_|
 |_|\_\___|\_/\___|_|   |_||_|\_,_|_| |_|  \_, | \__,_|_||_\__,_| |_|\_\___|\_/\___|_|     \_/\_/\___/_| |_|  \_, (_)
                                           |__/                                                               |__/                                                    
                                 __     __            _               _   ___  
                                 \ \   / /__ _ __ ___(_) ___  _ __   / | / _ \ 
                                  \ \ / / _ \ '__/ __| |/ _ \| '_ \  | || | | |
                                   \ V /  __/ |  \__ \ | (_) | | | | | || |_| |
                                    \_/ \___|_|  |___/_|\___/|_| |_| |_(_)___/ 
                                                                                   

                                                                               
                                                                                                                                                                                                                                                                                                                                 
'''
print(spider)

target_list = ["وسایل آرایشی، بهداشتی و درمانی"]
trust_list = []
finallist = []


def opener(x):
    try:
        time.sleep(0.5)
        wait = WebDriverWait(driver, 0.9)
        driver.get(x) # Get the fully rendered page source
        try: 
            button = wait.until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "آرایشی")))
        except:
            print(f"Wasn't a button match: {x}")
            return
        try:
            if button:
                for each in button:
                    try:
                        each_text = each.text
                    except:
                        print("sth wrong with getting text")
                    print("page_type is: ", each_text)
                    if each_text in target_list:
                        trust_list.append(x)
                        console.log(f"Match Found at: {x}")
                        break
                    else:
                        print(f"No match found: {x}")
            else:
                print(f"Button not found on page: {x}")
            return
        except:
            print(f"sth wrong when checking for matches on {x}")
            return
    except Exception as e:
        print(f"An error occurred while processing {x}: {e}")
        return




# Define a function to scroll down and load more results
def scroll_to_bottom():
    # Scroll down to the bottom of the page using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

with console.status("[blink bold red underline on white]Initializing...", spinner='betaWave') as status:
    # Set up the Selenium WebDriver for your preferred browser
    driver = webdriver.Firefox(options=myoptions)  

    # Navigate to the web page
    url = 'https://divar.ir/s/iran?q=%D8%AA%D8%B1%D8%A7%D8%B3%D8%AA'  # Replace with the URL of the page you want to scrape
    driver.get(url)

    article_links = []
    # Use WebDriverWait to wait for elements to load
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed

    page_height = driver.execute_script("return document.body.scrollHeight")

loop_counter = 0
button_press_counter  =  0 
article_links_counter = 0 
with console.status("[blink2 bold green]Scraping...", spinner='aesthetic') as status:    
    while True:
        article_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class=""]')))
        try:
            driver.find_element(By.CLASS_NAME, "post-list__load-more-btn-container-dcbb2").click()
            button_press_counter += 1
        except:    
            for i, element in enumerate(article_list):
                article_links.append(unquote(element.get_attribute('href').strip()))
                article_links_counter += 1
            # Scroll down to the bottom of the page
            scroll_to_bottom()

            # Wait for a few seconds to allow new content to load (customize the sleep time)
            time.sleep(1)  # Adjust this delay as necessary

            # Get the new page height
            new_page_height = driver.execute_script("return document.body.scrollHeight")

            # Check if the page height has not changed, indicating the end of loading
            if new_page_height == page_height:
                break
            
            # Update the page height
            page_height = new_page_height
            console.log(f"No. of Links found: {article_links_counter}")

 
article_links = list(dict.fromkeys(article_links))
print(article_links)
article_links_counter = len(article_links)
console.log(f"No. of Links found: {article_links_counter}")
print("Done here!")
print("NO. of more button press: ", button_press_counter)

today = str(date.today())
all_list = []
for each in article_links:
    encoded_url = quote(each, safe=':/')
    all_list.append(encoded_url)
with open(f'all-links-{today}.csv','w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for each in all_list:
        writer.writerow([each])

for i in track(article_links, description="Checking links"):
    opener(i)

for each in trust_list:
    encoded_url = quote(each, safe=':/')
    finallist.append(encoded_url)

finallist = list(dict.fromkeys(finallist))
print(finallist)
driver.quit()
console.log(f"Total No. of unique final links: {len(finallist)}")

#write the final results to a CSV file
with open(f'Charlotte-result-{today}.csv','w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for each in finallist:
        writer.writerow([each])
