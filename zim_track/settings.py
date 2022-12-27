# for Chrome driver 
from shutil import which

BOT_NAME = 'zim_track'

SPIDER_MODULES = ['zim_track.spiders']
NEWSPIDER_MODULE = 'zim_track.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

## ScrapeOps API Key
SCRAPEOPS_API_KEY = '05417a12-6aa9-4730-a086-480d5cd5f55e' ## Get Free API KEY here: https://scrapeops.io/app/register/main

## Enable ScrapeOps Proxy
SCRAPEOPS_PROXY_ENABLED = True

# Add In The ScrapeOps Monitoring Extension
EXTENSIONS = {
'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
}


DOWNLOADER_MIDDLEWARES = {

    ## ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    ## Proxy Middleware
    'zim_track.middlewares.ScrapeOpsProxyMiddleware': 725,
    
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1
FEED_EXPORT_ENCODING = 'utf-8'

#selenium
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS=['--headless']  
  
DOWNLOADER_MIDDLEWARES = {
     'scrapy_selenium.SeleniumMiddleware': 800
     }
