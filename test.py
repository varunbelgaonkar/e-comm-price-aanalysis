#importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
import time

#creating a driver
driver = webdriver.Chrome(r'C:\Users\varun\OneDrive\Documents\python projects\chromedriver.exe')
driver.implicitly_wait(10)
#function to scrape amazon site
def get_amaz_values(item):	
	url = 'https://www.amazon.in/'	
	#getting the webpage
	driver.get(url)
	#entering product name in search bar
	driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']").send_keys(item)
	#clicking search button
	driver.find_element(By.XPATH, "//input[@value='Go']").click()
	#selecting brand(specific to mobile category)
	brand = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Oppo']")))
	brand.click()
	try:
		ele = driver.find_element(By.XPATH, "//ul[@class='a-pagination']/li[6]")
	except NoSuchElementException as e:
		print(e)
	
	url_list = []
	#products_list = []
	#prices_list = []
	product_name = []
	prices = []
	
	#looping over multiple pages
	for page in range(int(ele.text)):
		page_ = page+1
		url_list.append(driver.current_url)
		#getting product name
		prod_name_list = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
		#getting product prices
		prod_prices_list = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")
		#appending text 
		for product in prod_name_list:
			product_name.append(product.text)
		for price in prod_prices_list:
			prices.append(price.text)
		try:
			driver.find_element(By.XPATH, "//li[@class='a-last']").click()
			print("page " + str(page_) + " is grabbed.")
			print(driver.current_url)
		except NoSuchElementException:
			print("All pages are collected!")
		time.sleep(5)
	#updating values in excel sheet	
	wb = Workbook()
	sheet = wb.active
	sheet["A1"] = "Product name"
	sheet["B1"] = "Product price"
	
	for data in zip(product_name, prices):
		sheet.append(data)
	
	wb.save("amazon_products.xlsx")
	print("All data collected!! >> File saved.")

	driver.quit()
