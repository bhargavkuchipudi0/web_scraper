import datetime
 
with open('/home/bhargav_kuchipudi/BHARGAV/PYTHON/WEB_SCRAPER/scrapers/output.txt','w') as outFile:
    outFile.write(str(datetime.datetime.now()) + '\n')