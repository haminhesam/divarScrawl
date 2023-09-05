from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

target_list = ['مراقبتی پوست و مو', 'لوازم آرایشی و زیبایی', 'پورسانتی/درصدی']

def opener(x):
    try:    
        r = requests.get(x).text
        r = BeautifulSoup(r, 'html.parser')
        page_type = r.find('a', attrs={"class": "kt-unexpandable-row__action kt-text-truncate"})
        page_type2 = r.find('p', attrs={"class": "kt-unexpandable-row__value"})
        if not (type(page_type) is None and type(page_type2) is None):
            try:
                page_type = page_type.text
            except:
                print("not in type 1")
            try:
                page_type = page_type2.text
            except:
                print("not in type 2")

        print(page_type)
        if (page_type in target_list):
            return True
        else:
            return False
    except: 
        print("http failure")

    
    



# Set up the Selenium WebDriver for your preferred browser
driver = webdriver.Firefox()  # You can use other browsers by changing this line

# Navigate to the web page
url = 'https://divar.ir/s/iran?q=%D8%AA%D8%B1%D8%A7%D8%B3%D8%AA'  # Replace with the URL of the page you want to scrape
driver.get(url)

# Define a function to scroll down and load more results
def scroll_to_bottom():
    # Scroll down to the bottom of the page using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

page_height = driver.execute_script("return document.body.scrollHeight")

# Scroll down and wait for more results until there are no more
while True:
    # Scroll down to the bottom of the page
    scroll_to_bottom()
    
    # Wait for a few seconds to allow new content to load (customize the sleep time)
    time.sleep(2)  # Adjust this delay as necessary
    
    # Get the new page height
    new_page_height = driver.execute_script("return document.body.scrollHeight")
    
    # Check if the page height has not changed, indicating the end of loading
    if new_page_height == page_height:
        break
    
    # Update the page height
    page_height = new_page_height

# Extract article links
article_links = []
article_list = driver.find_elements(By.TAG_NAME, 'a')
for i, element in enumerate(article_list):
    print(i)
    print(element.text)
    article_links.append(element.get_attribute('href'))
# You now have the article links in the 'article_links' list
print(article_links)
# Close the WebDriver when done
driver.quit()
new_article_list = []
with Bar('Loading Pages', max=len(article_links)) as bar:    
    for i, element in enumerate(article_links):
        print()
        print(element)
        if (opener(element)):
            new_article_list.append(element)
            print("found one")
        else:
            print("%s failed, trying next" %i)
        bar.next()
        print("\nsuccess: ", len(new_article_list))
    
    

print("finish", new_article_list)

