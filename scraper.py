from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from lxml import html
from lxml import etree
from io import StringIO
import pandas as pd
import numpy as np
dateFormat = '%Y-%m-% %H:%M:%S'
fileDate = '%Y%m%d%H%M'
filePath = '/home/noswald/Documents/PersonalScraper/'
chromeDriverPath = '/home/noswald/Documents/PersonalScraper/chromedriver'
searchValue = 'wallet'

searchPage = 'http://patft.uspto.gov/netahtml/PTO/search-adv.htm'
queryID = 'mytextarea'
searchButtonValue = 'Search'
yrsDropDownValue = 'PTXT'
display = Display(visible=0,size=(800,600))
display.start()
browser = webdriver.Chrome(chromeDriverPath)
browser.get(searchPage)
inputElement = browser.find_element_by_id(queryID)
inputElement.send_keys(searchValue)
inputElement.submit()
html_source = browser.page_source
curDT = datetime.now()
datepulled = curDT
t = curDT.strftime('%Y%m%d%H%M')
#uncomment if writing html file to directory
#f = open(filePath+'test1_' + t + '.html','w')
#f.write(html_source)
#f.close()
tree = html.parse(StringIO(html_source))

#add logic to pull correct end range (1-length of initial number of rows in table)
endRow = len(tree.xpath('//table[1]//tr'))-1
patentRank = [tree.xpath('//table[1]//tr[' + str(x) + ']/td[1]//text()')[0] for x in range(2,endRow)]
patentNumber = [tree.xpath('//table[1]//tr[' + str(x) + ']/td[2]//text()')[0] for x in range(2,endRow)]
patentTitle = [tree.xpath('//table[1]//tr[' + str(x) + ']/td[4]//text()')[0] for x in range(2,endRow)]
patentLink = ['http://patft.uspto.gov' + tree.xpath('//table[1]//tr[' + str(x) + ']/td[4]/a/@href')[0] for x in range(2,endRow)]

#loop over next page
while len(tree.xpath("//form[@name='srchForm']//input[starts-with(@name,'NextList')]"))>0:
    inputElement = browser.find_element_by_xpath("//form[@name='srchForm']//input[starts-with(@name,'NextList')]")
    time.sleep(2)
    inputElement.click() #try clicking button
    #add logic to pull new rank, number, title, and link and then append to existing data columns
    html_source = browser.page_source
    curDT = datetime.now()
    datepulled = curDT
    #uncomment if writing html file to directory
    #f = open(filePath+'test1_' + t + '.html','w')
    #f.write(html_source)
    #f.close()
    tree = html.parse(StringIO(html_source))
    endRow = len(tree.xpath('//table[1]//tr'))-1
    patentRank += [tree.xpath('//table[1]//tr[' + str(x) + ']/td[1]//text()')[0] for x in range(2,52)]
    patentNumber += [tree.xpath('//table[1]//tr[' + str(x) + ']/td[2]//text()')[0] for x in range(2,52)]
    patentTitle += [tree.xpath('//table[1]//tr[' + str(x) + ']/td[4]//text()')[0] for x in range(2,52)]
    patentLink += ['http://patft.uspto.gov' + tree.xpath('//table[1]//tr[' + str(x) + ']/td[4]/a/@href')[0] for x in range(2,52)]
    time.sleep(3)
    #keep re-creating dictionary and csv file with current data
    patentDict = {'Rank':patentRank, 'PatentNumber':patentNumber, 'PatentTitle':patentTitle, 'PatentLink':patentLink}
    patentFrame = pd.DataFrame.from_dict(patentDict)
    patentFrame.to_csv(filePath+'testTabDelim_'+t+'.txt',sep='\t')

browser.quit()
display.stop()
#create full Dictionary after all pages have been extracted
patentDict = {'Rank':patentRank, 'PatentNumber':patentNumber, 'PatentTitle':patentTitle, 'PatentLink':patentLink}
patentFrame = pd.DataFrame.from_dict(patentDict)
patentFrame.to_csv(filePath+'testTabDelim_'+t+'.txt',sep='\t')
print("Finished Scraping")
