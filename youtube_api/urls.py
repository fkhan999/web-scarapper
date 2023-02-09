"""youtube_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from rest_framework.authtoken import views
from api.serializers import YoutubeSerializers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('user.urls')),
]

#below is aync code to

from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor


#jobstores = {'mongo': {'type': 'mongodb'},'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'ap': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler()



def youtube_job():
    c=0
    from selenium import webdriver
    #import pandas as pd
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait 
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    chrome_options = Options()
    #chrome_options.add_experimental_option("detach", True)
    driver=webdriver.Chrome(chrome_options=chrome_options)
    import urllib.parse
    import time,json
    driver.get("https://www.youtube.com/results?search_query=music&sp=CAISBAgBEAE%253D")
    #time.sleep(5)
    driver.maximize_window()
    for x in range(10):
        ActionChains(driver).key_down(Keys.END).key_up(Keys.END).perform()
        time.sleep(2)
        user_data = driver.find_elements(By.XPATH,'//*[@id="video-title"]')
        links = []
        for i in user_data:
            a=i.get_attribute('href')
            if a is None:
                continue
            links.append(a)
    wait = WebDriverWait(driver, 10)
    for x in links:
        y="https://mattw.io/youtube-metadata/?url="+urllib.parse.quote(x)+"&submit=true"
        driver.get(y)
        a = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='snippet']/pre/code"))).text
        a=json.loads(a)
        v_id = x.strip('https://www.youtube.com/watch?v=')
        try:
            thumbnail=a['thumbnails']['maxres']['url']
        except:
            try:
                thumbnail=a['thumbnails']['standard']['url']
            except:
                thumbnail=a['thumbnails']['high']['url']
        desc=a["description"]
        if desc=="":
            desc="No description"
        serializer=YoutubeSerializers(data={"id":v_id,"title":a['title'],"description":desc,"thumbnail":thumbnail,"datetime":a['publishedAt']})
        if not serializer.is_valid():
            print({'error':serializer.errors,"message":"Please provide correct data"})
            continue
        serializer.save()
        print("saved",c)
        c+=1
    print("jobcompleted")
def youtube_job1():
    print("hello")

scheduler.configure(executors=executors, job_defaults=job_defaults)
#Job will run every hour
scheduler.add_job(youtube_job,'interval',minutes=60)
#job will run on startup
from datetime import datetime, timedelta, timezone

scheduler.add_job(youtube_job, "date", run_date=datetime.now(timezone.utc) + timedelta(seconds=10))
scheduler.start()


