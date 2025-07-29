"""
The site consists of one page with an infinite scroll.
Scroll down to the very bottom to reveal all tags and then scrape
"""

import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

TARGET_URL = 'https://www.brewersassociation.org/directories/breweries/'
HEADERS = ["name","addr","city","state","phone"]
ENTRY_XPATHS = [
	".//h2[contains(@itemprop, 'name')]", # name
	".//p[contains(@itemprop, 'streetAddress')]", # addr
	".//span[contains(@itemprop, 'addressLocality')]", # city
	".//span[contains(@itemprop, 'addressRegion')]", # state
	".//span[contains(@itemprop, 'telephone')]" # phone
]

def main():
	driver = init_selenium()
	driver.get(TARGET_URL)
	time.sleep(5)
	scroll_until_bottom(driver)
	print("Reached Bottom")
	time.sleep(5)
	save_data(scrape_content(driver))

def init_selenium():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--start-maximized")
	return webdriver.Chrome(
		service=ChromeService(
			executable_path=ChromeDriverManager().install(),
		),
		options=chrome_options
	)

def scroll_until_bottom(driver):
	old_height = 0
	new_height = 1
	while new_height != old_height:
		old_height = new_height
		new_height = scroll_down(driver)
		print(new_height)

def scroll_down(driver, pause=.5):
	# scrolls down and returns new scroll height
	for _ in range(driver.get_window_size()['height']):
		driver.find_element(By.XPATH, '//body').send_keys(Keys.DOWN)
	
	time.sleep(pause)
	return driver.execute_script("return document.body.scrollHeight")

def scrape_content(driver):
	# scrape visible content
	tags = driver.find_elements(By.XPATH, "//*[contains(@class, 'company-listing')]")
	return [HEADERS] + list(map(create_entry, tags))

def create_entry(tag):
	# converts a tag to a csv entry
	return list(map(lambda x: get_property(tag, x), ENTRY_XPATHS))

def get_property(tag, xpath):
	# extracts text from propetry but returns '' if not found
	try:
		return tag.find_element(By.XPATH, xpath).text
	except NoSuchElementException:
		return ''

def save_data(data):
	with open('brewers_association_addresses.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(data)

main()
