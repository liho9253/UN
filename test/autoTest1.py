from scrapy import cmdline
import datetime
import time
import shutil
import os

recoderDir = r"crawls"
ckeckFile = 'running.txt'

startTime = datetime.datetime.now()
print(f"startTime = {startTime}")

i = 0
miniter = 0
while True:
    if os.path.isfile(ckeckFile) == False:
        isExsit = os.path.isdir(recoderDir)
        print(f"mySpider not running, ready to start. isExsit:{isExsit}")
        
        if isExsit:
          removeRes = shutil.rmtree(recoderDir) # 刪除續爬目錄crawls及目錄下所有文件
          print(f"At time:{datetime.datetime.now()}, delete res:{removeRes}")
        else:
          print(f"At time:{datetime.datetime.now()}, Dir:{recoderDir} is not exsit.")
        time.sleep(20)
        clawerTime = datetime.datetime.now()
        waitTime = clawerTime - startTime
        print(f"At time:{clawerTime}, start clawer: mySpider !!!, waitTime:{waitTime}")
        cmdline.execute('scrapy crawl mySpider -s JOBDIR=crawls/storeMyRequest'.split())
        break #爬蟲結束之後，退出腳本
        
    else:
        print(f"At time:{datetime.datetime.now()}, mySpider is running, sleep to wait.")
        
    i += 1
    time.sleep(600)    # 每10分鐘檢查一次
    miniter += 10
    
    if miniter >= 1440:  # 等待滿24小時，自動退出監控腳本
      break