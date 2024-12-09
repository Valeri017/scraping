#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 23:37:46 2022

@author: Valeriy
"""
# Скрипт парсит ресурс ivi, страницу "Советское кино". И сортирует фильмы по рейтингу. Данную информацию
# можно записать в txt или в json
# Для корректной работы скрипта, нужно вызвать одну из generate функций передав словарь age_rating.
# Или раскоментировать последнюю строку print(age_rating)
# Время выполнения около 5 минут

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import pprint
from bs4 import BeautifulSoup 
import pandas as pd
import json



def hand_over_url(url):
    """
    принимает URL
    """
    try:
        html = urlopen(url)
        return html
    except HTTPError as e:
        return print(e)
    except URLError as e:
        return print("Сервер отключен или URL не найден")
    

def get_name_move(num:int) -> str:
    """
    Скрапинг имен фильмов
    """
    none_name_list=[29,59,89,119,149]
    try:
        if num in none_name_list:
            num+=1
        if num>=0 and num < 29:
            soup = BeautifulSoup(hand_over_url('https://www.ivi.ru/movies/sovetskoe_kino/').read(), 'lxml')
        elif num >= 30 and num < 59:
            soup = BeautifulSoup(hand_over_url('https://www.ivi.ru/movies/sovetskoe_kino/page2').read(), 'lxml')
        elif num >= 60 and num < 89:
            soup = BeautifulSoup(hand_over_url('https://www.ivi.ru/movies/sovetskoe_kino/page3').read(), 'lxml')
        elif num >= 90 and num < 119:
            soup = BeautifulSoup(hand_over_url('https://www.ivi.ru/movies/sovetskoe_kino/page4').read(), 'lxml')
        elif num >= 120 and num < 149:
            soup = BeautifulSoup(hand_over_url('https://www.ivi.ru/movies/sovetskoe_kino/page5').read(), 'lxml')
        else:
            soup = BeautifulSoup(hand_over_url('https://www.ivi.ru/movies/sovetskoe_kino/page6').read(), 'lxml')
        
        li_all = soup.find_all('li',class_="gallery__item gallery__item_virtual")
        get_inf = li_all[num].find('span',class_= "nbl-slimPosterBlock__titleText").get_text()
    except AttributeError: 
        return print('Больше фильмов нет')
    return get_inf 


link = 'https://www.ivi.ru/movies/sovetskoe_kino/'
zero_rating = []
six_rating = []
twelve_rating = []
sixtin_rating = []
for i in range(1,7):
    soup = BeautifulSoup(hand_over_url(link + 'page'+str(i)).read(), 'lxml')
    li_all = soup.find_all('li',class_="gallery__item gallery__item_virtual")
    for j in range(len(li_all)):
        if li_all[j].find('div',class_= "nbl-ageBadge nbl-ageBadge nbl-ageBadge_value_0 nbl-poster__nbl-ageBadge"):
            zero_rating.append(get_name_move(j))
        elif li_all[j].find('div',class_= "nbl-ageBadge nbl-ageBadge nbl-ageBadge_value_6 nbl-poster__nbl-ageBadge"):
            six_rating.append(get_name_move(j))
        elif li_all[j].find('div',class_= "nbl-ageBadge nbl-ageBadge nbl-ageBadge_value_12 nbl-poster__nbl-ageBadge"):
            twelve_rating.append(get_name_move(j))
        elif li_all[j].find('div',class_= "nbl-ageBadge nbl-ageBadge nbl-ageBadge_value_16 nbl-poster__nbl-ageBadge"):
            
            sixtin_rating.append(get_name_move(j))

lst_rating = ['zero_plus', 'six_plus', 'twelve_plus','sixtin_plus']
age_rating = dict(zip(lst_rating,(zero_rating,six_rating,twelve_rating,sixtin_rating)))



def generate_json(age_rating):
    with open('ivi_script.json','w') as f:
        age_rating = dict(zip(lst_rating,(zero_rating,six_rating,twelve_rating,sixtin_rating)))
        json.dump(age_rating,f)


def generate_txt(age_rating):
    with open('ivi_script.txt','w') as f:
        f.write(str(age_rating))
        
# print(age_rating)