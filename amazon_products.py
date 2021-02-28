from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

driver = webdriver.Chrome(r'C:\Users\varun\OneDrive\Documents\python projects\chromedriver.exe')

def get_url_list():
	#item = input("Enter item to be searched: ")
	url = 'https://www.amazon.in/'
	driver.get(url)
	driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']").send_keys("oppo mobile")
	driver.find_element(By.XPATH, "//input[@value='Go']").click()
	driver.implicitly_wait(3)
	brand = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'Oppo']")))
	brand.click()
	driver.implicitly_wait(3)
	ele = driver.find_element(By.XPATH, "//ul[@class='a-pagination']/li[6]")
	
	url_list = []
	
	for i in range(int(ele.text)):
		page_ = i+1
		url_list.append(driver.current_url)
		try:
			driver.find_element(By.XPATH, "//li[@class='a-last']").click()
			print("page " + str(page_) + " is grabbed.")
			print(driver.current_url)
		except NoSuchElementException:
			print("All pages are collected!")
		driver.implicitly_wait(5)
	
	with open("amz_url_list.txt", 'w') as f:
		for url in url_list:
			f.write(f'{url}\n')
	return url_list
	
def get_values():
	urls = get_url_list()
	products_list = []
	prices_list = []
	for url in urls:
		driver.get(url)
		driver.implicitly_wait(10)	
		prod_names_list = driver.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
		#prod_names_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")))
		products_list = products_list + prod_names_list	
		driver.implicitly_wait(10)	
		prod_prices_list = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")
		#prod_prices_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-price-whole']")))
		prices_list = prices_list + prod_prices_list
		driver.implicitly_wait(10)
	print(len(products_list))
	print(len(prices_list))
	products = []
	prices = []
	try:
		for product in products_list:
			products.append(product.text)
	except StaleElementReferenceException as e:
		print(e)
	try:
		for price in prices_list:
			prices.append(price.text)
	except StaleElementReferenceException as e:
		print(e)
	print(products)
	print(prices)

	wb = Workbook()
	sheet = wb.active
	sheet["A1"] = "Product Name"
	sheet["B1"] = "Price"
	for data in zip(products, prices):
		sheet.append(data)
	wb.save("amazon_products.xlsx")



get_values()