from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from openpyxl import Workbook
import time


driver = webdriver.Chrome(r'C:\Users\varun\OneDrive\Documents\python projects\chromedriver.exe')
def get_flipkart_values(item):
	url = 'https://www.flipkart.com/'
	
	#getting the page
	driver.get(url)
	driver.implicitly_wait(5)
	#searching the product
	driver.find_element(By.XPATH, "//input[@name='q']").send_keys(item)
	try:
		#closing dialogue box and clicking search button
		driver.find_element(By.XPATH, "//button[@class='_2KpZ6l _2doB4z']").click()
		driver.find_element(By.XPATH, "//button[@class='L0Z3Pu']").click()
	except NoSuchElementException as e:
		print(e)
	else:
		driver.find_element(By.XPATH, "//button[@class='L0Z3Pu']").click()
	driver.implicitly_wait(5)
	#getting number of pages
	element = driver.find_element(By.XPATH, "//div[@class='_2MImiq']/span")
	pages = element.text.split(" ")[3]
	print(pages)
	
	url_list = []
	product_name = []
	prices = []
	
	driver.implicitly_wait(5)
	#looping over multiple pages
	for page in range(int(pages)):
		page_ = page + 1
		url_list.append(driver.current_url)
		#getting product name
		prod_name_list = driver.find_elements(By.XPATH, "//div[@class='_4rR01T']")
		#getting product price
		prod_prices_list = driver.find_elements(By.XPATH, "//div[@class='_30jeq3 _1_WHN1']")
		for product in prod_name_list:
			product_name.append(product.text)
		for price in prod_prices_list:
			prices.append(price.text)
	
		#clicking on next button
		try:
			driver.find_element(By.XPATH, "//a[@class='_1LKTO3']/span[contains(text(),'Next')]").click()
		except NoSuchElementException as e:
			print(e)
		except ElementClickInterceptedException as e:
			print(e)
		print("page " + str(page_) + " is grabbed.")
		print(driver.current_url)	
		time.sleep(5)
		
	
	with open("fkrt_url_list.txt", 'w') as f:
		for url in url_list:
			f.write(f'{url}\n')
	
	wb = Workbook()
	sheet1 = wb.active
	sheet1["A1"] = "Product Name"
	sheet1["B1"] = "Price"
	
	for data in zip(product_name, prices):
		sheet1.append(data)
	
	wb.save("flipkart.xlsx")
	print("All data collected!! >> File saved.")
	driver.quit()	

