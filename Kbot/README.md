# KBOT - Discord bot from Korean Drama fans

### Video demo - https://youtu.be/BTvHOveNX44

### Description:

Kbot is a discord bot that will webscrape an entertainment website to find information corresponding
to a drama that the user enters in as a command with the bot. The bot can also provide suggestions if the user asks
for one by pulling the information of a random drama on the top dramas page. Currently the bot focuses on korean dramas.

The bot consists of two files and was made using Python 3.8.6. The purpose of each file will be elaborated below.

#### Kdrama_scraper.py:

This file uses a method called webscraping to collect information from websites in a browser. The library used to achieve
this is beautifulsoup4. So based on the name of the drama entered, the program searches the website for dramas with similar key words
and then picks the one with the highest rank to scrape. The program will retrieve the chosen drama's webpage and extract the useful information
such as the synopsis, cast, and ratings.

#### Bot.py

This file is more simple in its functionality with its main purpose being to use discord's API to let the user's commands in a message bar utilize the
Kdrama_scraper program. Depending on the command entered by the user, a specific function will be called. If the user asks for a suggestion the getstuff function
is called. However if a suggestion is asked the getSuggest function is called

## Commands that can be used:

### Retrieve specific drama:

/kbot {drama_name}

### Get a random suggestion:

/kbot suggest


#### Libraries used

bs4 - (beautifulsoup)
discord
discord.ext


#### Resource link for scraping:

https://mydramalist.com/

#### Source code for Kdrama_scraper:
```
from bs4 import BeautifulSoup as bs
import requests
import sys
import random

#ACCESS SEARCH PAGE AND DETERMINE WHETHER THERE ARE VALID RESULTS

def getTop(soup):
    search_results = soup.find('div', class_='col-lg-8 col-md-8')
    boxes = search_results.find_all('div', class_='box')
    ranks = []

    for box in boxes:
        try:
            rank = box.find('div', class_='ranking pull-right').text.strip()[1:]
            ranks.append(int(rank))

        except:
            ranks.append(999999)
            pass

    min_rank = ranks.index(min(ranks))
    return boxes[min_rank]

#FIND A RANDOM DRAMA PAGE
def getRandom(soup):
    search_results = soup.find('div', class_='col-lg-8 col-md-8')
    boxes = search_results.find_all('div', class_='box')
    random_number = random.randint(0, 19)

    return boxes[random_number]

#FIND TOP RANK OF SEARCH RESULTS
def getTopPage(soup):
    highest_rank = getTop(soup)
    href = highest_rank.find('a').get('href')
    main_url = 'https://mydramalist.com/' + href
    return main_url

def getRandomPage(soup):
    random_box = getRandom(soup)
    href = random_box.find('a').get('href')
    main_url = 'https://mydramalist.com/' + href
    print(main_url)
    return main_url

def getImg(drama_page):
    cover = drama_page.find('div', class_='film-cover')
    img = cover.find('img', class_='img-responsive')
    src = img.get('src')
    return src

#ACCESS DRAMA PAGE OF FIRST RESULT IF THERE
def getstuff(drama):
    # GET URL AND USER INPUT
    url = 'https://mydramalist.com/search?q='

    #search_query = input("Drama name: ").replace(" ", "+")
    search_query = drama.lower()
    page = requests.get(url + search_query)
    soup = bs(page.text, 'html.parser')

    main_url = getTopPage(soup)
    drama_page = bs(requests.get(main_url).text, 'html.parser')

    #SCRAPE RELEVANT DATA
    #Rating, Cast, Description, image
    img = getImg(drama_page)

    drama_info = drama_page.find('div', class_='col-sm-8')
    title = drama_page.find('h1', class_='film-title').text

    #show synopsis
    synopsis = drama_info.find('div', class_='show-synopsis').text.strip()
    print(f'\nSynopsis: \n{synopsis}\n')

    #Rating
    rating = drama_info.find('div', class_='hfs').text.strip()
    print(rating)

    #cast
    cast_info = drama_page.find('div', class_='p-a-sm')
    cast_list = cast_info.find('ul', class_='list no-border p-b')
    cast_members = cast_list.find_all('li', class_='list-item col-sm-4')
    members = []

    print('\nCast:')
    for member in cast_members:
        member_profile = member.find('div', class_='col-xs-8 col-sm-7 p-a-0')
        member_name = member_profile.find('a', class_='text-primary text-ellipsis').text.strip()
        members.append(member_name)
        print(member_name)

    return synopsis, rating, members, img, title


def getSuggest():

    # GET URL AND USER INPUT
    url = 'https://mydramalist.com/shows/top'

    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    random_page = getRandomPage(soup)
    drama_page = bs(requests.get(random_page).text, 'html.parser')

    #SCRAPE RELEVANT DATA
    #Rating, Cast, Description, image
    img = getImg(drama_page)

    drama_info = drama_page.find('div', class_='col-sm-8')
    title = drama_page.find('h1', class_='film-title').text

    #show synopsis
    synopsis = drama_info.find('div', class_='show-synopsis').text.strip()
    print(f'\nSynopsis: \n{synopsis}\n')

    #Rating
    rating = drama_info.find('div', class_='hfs').text.strip()
    print(rating)

    #cast
    cast_info = drama_page.find('div', class_='p-a-sm')
    cast_list = cast_info.find('ul', class_='list no-border p-b')
    cast_members = cast_list.find_all('li', class_='list-item col-sm-4')
    members = []

    print('\nCast:')
    for member in cast_members:
        member_profile = member.find('div', class_='col-xs-8 col-sm-7 p-a-0')
        member_name = member_profile.find('a', class_='text-primary text-ellipsis').text.strip()
        members.append(member_name)
        print(member_name)

    return synopsis, rating, members, img, title
```
