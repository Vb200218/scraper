from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time


# class info:
#     def __init__(self,course_link,image_link,course_name,organistaion_name,no_reg,time_left,hashtags):
#         self.course_link=course_link
#         self.image_link=image_link
#         self.course_link

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
driver = webdriver.Chrome('E:/Internship/hackathon/chromedriver(1).exe', options=option)
 
driver.get("https://unstop.com/all-opportunities?filters=open&types=oppstatus")

elem=driver.find_element_by_tag_name("body")



no_of_pagedowns = 100

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1




soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content

# print(soup)
body=soup.find("body")
div=body.find("div")
main=div.find("main")
section=main.find("section")
inner_div=section.find("div",class_="right_sect")
app_list=inner_div.find("app-opportunity-listbox")
a=app_list.find_all("a")
course_link=[]
image_link=[]
course_name=[]
organistaion_name=[]
no_reg=[]
time_left=[]
hashtags=[]
fee=[]
for anchor in a:
    link=anchor.get("href")
    image_tag=anchor.find("img")
    img_link=image_tag.get("src")
    course=anchor.find("h2").text
    org_name=anchor.find("h3").text
    reg_strong=anchor.find_all("strong")
    for i in reg_strong:    
        numb_reg=i.text
        days_left=i.text
    tag=anchor.find_all("div",class_="tag")
    tags=[]
    for j in tag:    
        tags.append(j.text)
    price_em=anchor.find("div",class_="inr ng-star-inserted")
    if price_em!=None:
        price=price_em.text
    else:
        price=0
    
    course_link.append("https://unstop.com/"+str(link))
    image_link.append(img_link)
    course_name.append(course)
    organistaion_name.append(org_name)
    no_reg.append(numb_reg)
    time_left.append(days_left)
    hashtags.append(tags)
    fee.append(price)


z=pd.DataFrame({'course link' :course_link ,
              'image_link' : image_link,
              'course_name' : course_name,
              'organistaion_name':organistaion_name,
              'Registration':no_reg,
              'time_left':time_left,
              'hashtags':hashtags,
              'fee':fee})
           
z.to_csv("file.csv")