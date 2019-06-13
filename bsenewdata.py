#Complete Updation of Data for BSE
import csv
import numpy as np
import time
import pandas as pd
import xlwt
from fractions import Fraction
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC   
import datetime, timedelta
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os
from selenium.common.exceptions import NoSuchElementException

a=[];
y=[];
search_query=[]
y=pd.read_csv("/home/jinit/Downloads/SchemeIndexMapping.csv")

for i in range(0,len(y)):
	 if y["subgroup"].iloc[i]=="BSE" and y["Index_gp"].iloc[i]=="Equity":
	 	if "TRI" not in (y["IndexName"].iloc[i]):
		 	b=(y["IndexName"].iloc[i])
		 	a.append(b)
		 	# print(b,len(y))

for i in range(0,len(a)):
	try:
		
			x=datetime.datetime.now()
			y=datetime.datetime.now() - datetime.timedelta(days=8)
			# date=x.strftime("%d/%m/%Y")
			fromdate= y.strftime("%d/%m/%Y")
			todate  = x.strftime("%d/%m/%Y")
			# for i in range(0,len(a)):
			fp = webdriver.FirefoxProfile()
			fp.set_preference("browser.preferences.instantApply",True)
			fp.set_preference("browser.download.folderList", 2)
			fp.set_preference("browser.helperApps.alwaysAsk.force",False)
			fp.set_preference("browser.download.dir", "/home/jinit/Downloads/BSE/{}/".format(a[i]));
			fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")

			browser = webdriver.Firefox(firefox_profile=fp,executable_path=r'/home/jinit/Jinit/geckodriver-v0.24.0-linux64/geckodriver')
			browser.get("https://origin-www.bseindia.com/Indices/IndexArchiveData.html")
			
			index = browser.find_element_by_id("ddlIndex")
			index.click()
			new = Select(index)
			new.select_by_visible_text("{}".format(a[i]))
			fromDate = browser.find_element_by_id("txtFromDt")
			toDate   = browser.find_element_by_id("txtToDt")
			browser.execute_script("arguments[0].setAttribute('onkeypress','')", fromDate)
			browser.execute_script("arguments[0].setAttribute('onkeypress','')", toDate)
			fromDate.send_keys("{}".format(fromdate))
			toDate.send_keys("{}".format(todate))
			submit = browser.find_element_by_class_name("btn-default")
			submit.click()
			time.sleep(3)
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			# time.sleep(3)
			button = browser.find_element_by_class_name("iconfont")	
		
			form_element = browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[3]/div[2]/i")
			form_element.click()
			print("done for {}".format(a[i]) )
			browser.close()		
	except NoSuchElementException:
		print("Not found {}".format(a[i]))

	count=0
	with open('/home/jinit/Downloads/BSE/{}/CSVForDate(1).csv'.format(a[i]), 'r') as csvFile:
			reader = (csv.reader(csvFile))
			header = reader.next()
			for row in reader:

				b=row[0]
				newdate=pd.read_csv('/home/jinit/Downloads/BSE/{}/CSVForDate(1).csv'.format(a[i]),skiprows=1)	
				newdate.drop("Unnamed: 5",axis=1,inplace=True)
				try:
						with open('/home/jinit/Downloads/BSE/{}/CSVForDate.csv'.format(a[i]), 'r') as csvFile:
										reader = (csv.reader(csvFile))
										header = reader.next()
										for row in reader:
											c=row[0]
						# print(c)

						d1=datetime.datetime(int(datetime.datetime.strptime(b,'%d-%B-%Y').strftime("%Y")),int(datetime.datetime.strptime(b,'%d-%B-%Y').strftime("%m")),int(datetime.datetime.strptime(b,'%d-%B-%Y').strftime("%d")))
						d2=datetime.datetime(int(datetime.datetime.strptime(c,'%d-%B-%Y').strftime("%Y")),int(datetime.datetime.strptime(c,'%d-%B-%Y').strftime("%m")),int(datetime.datetime.strptime(c,'%d-%B-%Y').strftime("%d")))
						# print(d1>d2)
						# print(newdate.iloc[count-1])

						if(d1>d2):

								with open('/home/jinit/Downloads/BSE/{}/temp.csv'.format(a[i]), 'wb') as csvFile:
									filewriter = csv.writer(csvFile, delimiter=",")
									filewriter.writerow(newdate.iloc[count-1])
									# filewriter.
								print(newdate.iloc[count-1],a[i])


						
								filenames=["/home/jinit/Downloads/BSE/{}/CSVForDate.csv".format(a[i]),"/home/jinit/Downloads/BSE/{}/temp.csv".format(a[i])]
							 	with open('/home/jinit/Downloads/BSE/{}/new.csv'.format(a[i]), 'w') as outfile:
									 	    for fname in filenames:
									 	        with open(fname) as infile:
									 	            outfile.write(infile.read())
								os.remove("/home/jinit/Downloads/BSE/{}/temp.csv".format(a[i]))
								
								with open('/home/jinit/Downloads/BSE/{}/new.csv'.format(a[i])) as f:
  								  with open("/home/jinit/Downloads/BSE/{}/CSVForDate.csv".format(a[i]), "w") as f1:
   									    for line in f:
   									        f1.write(line)		 	            	

								os.remove('/home/jinit/Downloads/BSE/{}/new.csv'.format(a[i]))		

						count+=1
				except IndexError:
					print("Error")
				
			count=0
	os.remove('/home/jinit/Downloads/BSE/{}/CSVForDate(1).csv'.format(a[i]))	





