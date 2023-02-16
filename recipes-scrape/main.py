import requests
from bs4 import BeautifulSoup
import json

#============================STEP 1:We save the URL address so that the site does not block us during the parsing.=============================
#---------------------------------------------------------START-----------------------------------------------------------
# url='http://vkysnoprosto.ru/recepty/'
#
#
headers={
     'accept': '*/*',
     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
# req=requests.get(url,headers=headers)
# src=req.text
# with open('index.html','w',encoding='utf-8') as file:
#     file.write(src)
#---------------------------------------------------------END-----------------------------------------------------------



#============================STEP 2:We create a JSON file with a dictionary key - category name, value - link.=============================

#---------------------------------------------------------START-----------------------------------------------------------
with open('index.html',encoding='utf-8') as file:
    src=file.read()


list_cat_hrefs=[]
list_cat_names=[]
all_cat_dict={}
soup=BeautifulSoup(src,'lxml')
all_categories_hrefs=soup.find_all(class_='category-tile')
all_categories_names=soup.find_all('h3')
for href in all_categories_hrefs:
    item_href=href.get('href')
    list_cat_hrefs.append(item_href)
for name in all_categories_names:
    item_name=name.text.capitalize()
    list_cat_names.append(item_name)
all_cat_dict=dict(zip(list_cat_names,list_cat_hrefs))
with open('all_categories.json','w') as file:
    json.dump(all_cat_dict,file,indent=4,ensure_ascii=False)



#---------------------------------------------------------END-----------------------------------------------------------






#====================STEP 3:We create an HTML file for each category and collect the name of the dish and a link to the recipe from them.=============================

with open('all_categories.json') as file:
    all_categories=json.load(file)
count=0
all_recipes_dict={}
list_recipes_hrefs=[]
list_recipes_names=[]
for categories_name,categories_href in all_categories.items():
    rep=[',',' ']
    for item in rep:
        if item in categories_name:
            categories_name=categories_name.replace(item,'_')


    req=requests.get(url=categories_href,headers=headers)
    src=req.text

    with open(f'data/{count}_{categories_name}.html','w',encoding='utf-8') as file:
        file.write(src)

    with open(f'data/{count}_{categories_name}.html',encoding='utf-8') as file:
        src=file.read()

    soup=BeautifulSoup(src,'lxml')

    all_recipes_hrefs=soup.find_all(class_='archive-item-media-thumbnail fader-activator')
    all_recipes_names=soup.find_all(class_='entry-title')
    for href in all_recipes_hrefs:
        item_href=href.get('href')
        list_recipes_hrefs.append(item_href)
    for name in all_recipes_names:
        item_name=name.text
        list_recipes_names.append(item_name)

    count+=1
all_recipes_dict=dict(zip(list_recipes_names,list_recipes_hrefs))
with open('all_recipes.json', 'w') as file:
    json.dump(all_recipes_dict, file, indent=4, ensure_ascii=False)
#---------------------------------------------------------END-----------------------------------------------------------
