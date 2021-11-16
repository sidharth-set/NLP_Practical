# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 19:24:45 2021

@author: DELL
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import requests
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

chrome = webdriver.Chrome("E://chromedriver_win32//chromedriver.exe")
webdriver = chrome

webdriver.get('https://www.google.com/search?q=greensky+atlanta&sxsrf=AOaemvIC3SgwHaiuNr-iwl-3Y9hc7xOngA%3A1637071362590&ei=ArqTYZK3I5PWz7sP0aSEqA4&oq=greensky+atlanta&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyDQguEMcBENEDELADEEMyBwgAELADEENKBAhBGABQAFgAYIEGaAFwAngAgAEAiAEAkgEAmAEAyAEKwAEB&sclient=gws-wiz&ved=0ahUKEwiSwKeIhp30AhUT63MBHVESAeUQ4dUDCA4&uact=5')

#Reviewer,ReviewDate,ReviewRating,ReviewDescription,TotalReviewsByUser,webdriver_obj,thisreview =([],) * 7
Reviewer =[]
ReviewDate = []
ReviewRating =[]
ReviewDescription = []
TotalReviewsByUser = []
webdriver_obj = []
thisreview =[]
print('!!!')
time.sleep(3)
last_len = 0

def  get_reviews(thisreview):
    global last_len
    print("Don't Stop")
    for webdriver_obj in thisreview.find_elements_by_class_name("WMbnJf"):
        Name = webdriver_obj.find_element_by_class_name("Y0uHMb")
        Reviewer.append(Name.text)
        try:
            ReviewByuser = webdriver_obj.find_element_by_class_name("A503be")
            TotalReviewsByUser.append(ReviewByuser.text)
        except NoSuchElementException:
            TotalReviewsByUser.append("")
        star = webdriver_obj.find_element_by_class_name("fTKmHE99XE4__star")
        ReviewStar =star.get_attribute("aria-label")
        ReviewRating.append(ReviewStar)
        Date = webdriver_obj.find_element_by_class_name("dehysf")
        ReviewDate.append(Date.text)
        Body = webdriver_obj.find_element_by_class_name('Jtu6Td')
        try:
            webdriver_obj.find_element_by_class_name('review-snippet').click()
            s_32B = webdriver_obj.find_element_by_class_name('review-full-text')
            ReviewDescription.append(s_32B.text)
        except NoSuchElementException:
            ReviewDescription.append(Body.text)
        print("Yes..")
        element = webdriver_obj.find_element_by_class_name('PuaHbe')
        webdriver.execute_script("arguments[0].scrollIntoView();", element)
    print("ah!..Go")
    time.sleep(3)
    reviews = webdriver.find_elements_by_class_name("gws-localreviews__general-reviews-block")
    r_len = len(reviews)
    if r_len > last_len:
        last_len = r_len
        get_reviews(reviews[r_len-1])

    reviews = webdriver.find_elements_by_class_name("gws-localreviews__general-reviews-block")
    last_len = len(reviews)
    get_reviews(reviews[last_len-1])

    data = pd.DataFrame ( { 'Reviewer' : Reviewer, 'TotalReviewsByUser': TotalReviewsByUser,
                               'ReviewRating':ReviewRating,'ReviewDate':ReviewDate,
                               'ReviewDescription':ReviewDescription})

    data.to_csv('reviews.csv', index=False)    
    return data