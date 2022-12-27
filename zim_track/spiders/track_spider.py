import re
import json
import scrapy
from urllib.parse import urlencode
from zim_track.items import zimItem

from scrapy.item import Field, Item
from scrapy.loader import ItemLoader



#import selenium
from selenium import webdriver
import importlib.util
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pandas as pd
import pypyodbc as odbc # pip install pypyodbc
from datetime import datetime


#routes
excel_rute=r'C:/Users/andre/Desktop/Samsung/scrapy/scrapy_jafm/Master_BOL.csv'
htmls_scraped=r'C:/Users/andre/Desktop/Samsung/scrapy/scrapy_jafm/env/data/scrap/'
binary_location_firefox=r'C:/Program Files/Mozilla Firefox/firefox.exe'
src='file:///C:/Users/andre/Desktop/Samsung/scrapy/scrapy_jafm/env/data/scrap/src/idmod/'
data_base_access=r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=C:/Users/andre/Desktop/Samsung/scrapy/scrapy_jafm/zim.accdb;'

zimitem= zimItem()
class TrackSpider(scrapy.Spider):
       
    name = "track_spider"
    allowed_domains = ["https://www.zim.com/"]

    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        }  

    def get_zim_search_url(self, keyword):
        parameters = {"q": keyword}
        #var to will be to scrap
        return "https://www.zim.com/tools/track-a-shipment?" + urlencode(parameters)


    def start_requests(self):
        #import data of csv  
        data= pd.read_csv(excel_rute,header=None, skiprows=1)
        keyword_list = data[0].values.tolist()
        #keyword_list = ['ZIMUSEL766825']

        for keyword in keyword_list:
            
            zim_jobs_url = self.get_zim_search_url(keyword)
            yield SeleniumRequest(url=zim_jobs_url, callback=self.parse_search_results, wait_time=110, meta={
                'keyword': keyword,

            })

    def parse_search_results(self, response):
        #recive all documents scraped
        keyword=response.meta['keyword']
        print('-----------------*___*-----------------')
        Func = open(htmls_scraped+keyword+'.html',"w+",encoding='utf-8')
        #convert to string
        html=response.text
        # Adding input data to the HTML file
        Func.write(html)
        # Saving the data into the HTML file
        Func.close()
        
        #use selenium for de render html
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.binary_location = binary_location_firefox
        options.set_preference('dom.webnotifications.enabled', False)
        options.headless = True
        driver = webdriver.Firefox(options=options)
       
        driver.get(src+keyword+'.html')
        
        #save in local var
        num= keyword
        container= driver.find_element("xpath",'//*[@id="0_desktop_1_unitNo"]').text
        last_activity= driver.find_element("xpath",'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div[1]/div[3]/div/ul/li[1]/div[2]/div[1]/div[3]/div/div[2]').text
        location= driver.find_element("xpath",'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div[1]/div[3]/div/ul/li[1]/div[2]/div[1]/div[4]/div/div[2]').text
        date= driver.find_element("xpath",'//*[@id="0_desktop_5_activityDateTz"]').text
        voyage= driver.find_element("xpath",'/html/body/div[3]/div[2]/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div[1]/div[3]/div/ul/li[1]/div[2]/div[1]/div[6]/div/div[2]').text
        #init item for save csv de record log
        zimitem['Master_BL']= num
        zimitem['container']= container
        zimitem['last_activity'] = last_activity
        zimitem['location'] = location
        zimitem['date'] = date
        zimitem['voyage'] = voyage

        driver.quit()


        




        try: 
            conn = odbc.connect(data_base_access)
        except odbc.DatabaseError as e:
            print('Database Error:')    
            print(str(e.value[1]))
        except odbc.Error as e:
            print('Connection Error:')
            print(str(e.value[1]))

        """
        Create a cursor connection and insert records
        """

        sql_insert = '''
            INSERT INTO tracking_details ([Master_BL],[container],[last_activity],[location_c],[dates],[voyage])
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        fecha_dt = datetime.strptime(date, '%d-%b-%Y')
        #print(fecha_dt)
        fecha_str=fecha_dt.strftime('%d/%m/%Y')
        #print(fecha_str)
  
        
        #prueba de crear array de resultaso
        dld=[]
        dld.append(num)
        dld.append(container)
        dld.append(last_activity)
        dld.append(location)
        dld.append(date)
        dld.append(voyage)
    
        try:
            cursor = conn.cursor()
            cursor.execute(sql_insert,(num,container,last_activity,location,fecha_str,voyage))
            cursor.commit();    
        except Exception as e:
            cursor.rollback()
            print(str(e))
        finally:
            print('crawls is complete.')
            cursor.close()
            conn.close()

        yield zimitem