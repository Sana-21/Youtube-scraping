from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import time
import pandas as pd
driver = webdriver.Chrome()
url = 'https://www.youtube.com/@MasterChefWorld/videos'
driver.get(url)

SCROLL_PAUSE_TIME = 20

last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
    time.sleep(SCROLL_PAUSE_TIME)
    
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

titles = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
views = driver.find_elements(By.XPATH, '//*[@id="metadata-line"]/span[1]')
times = driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[2]' )
thumbnails = driver.find_elements(By.XPATH,'//*[@id="thumbnail"]/yt-image/img')


data = []
for i in range(len(titles)):
    title = titles[i].text
    view = views[i].text
    time_ = times[i].text
    thumbnail = thumbnails[i].get_attribute("src")
    
    data.append({
        "Title": title,
        "Views": view,
        "Time": time_,
        "Thumbnail URL": thumbnail
    })

df = pd.DataFrame(data)
df.to_csv("youtube_data.csv", index=False)

driver.quit()
