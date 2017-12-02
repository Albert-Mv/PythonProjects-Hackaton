import os
import shutil
import time
import HTMLParser

def verifyNewsCount():
    os.chdir("News")
    if len(os.listdir(os.getcwd())) > 10:
        min = 999999
        for dirname in os.listdir(os.getcwd()):
            if min > int(dirname):
                min = int(dirname)
        shutil.rmtree(os.getcwd()+"/"+str(min))
        os.chdir("../")
    else:
        os.chdir("../")
        return
    verifyNewsCount()

def launch():
    while True:
        print("Update!")
        time.sleep(15)
        HTMLParser.loadData()
        verifyNewsCount()

launch()
