"""
Parser of everything from the Russian reshebnik GDZ.RU
"""


__version__ = "0.1.0"


import bs4
import requests
import json
import ua


def getSchoolItems():
    """
    ### Allows you to get avaliable school subjects

    Subject name parsed from GDZ site, so run command and find your subject
    """
    # List
    schoolItemsList = []

    # UA
    useragent = ua.getRandomUserAgent()

    getGdzPage = requests.get("https://gdz.ru/", headers={'User-Agent': useragent['useragent']}).text
    wrappedPage = bs4.BeautifulSoup(getGdzPage, 'lxml')

    for schoolitem in wrappedPage.find_all('td', attrs={"class": "table-section-heading"}):
        ejectedUrl = schoolitem.find('a').get('href')
        schoolItemsList.append(str(ejectedUrl).replace('/', ''))

    try:
        schoolItemsList.pop(0)
    except IndexError:
        raise requests.ConnectionError

    return schoolItemsList


def get(type, jsonEnable=True, **args):
    # Lists
    bookList = []
    ErrorList = [
        "school item is null",
        "number is greater than 11 or null"
    ]

    # UA
    useragent = ua.getRandomUserAgent()

    if (type == 'books'):
        if (int(args.get("schoolclass")) <= 11):
            if ('schoolitem' in args):
                getGdzPage = requests.get(f'https://gdz.ru/class-{args["schoolclass"]}/{args["schoolitem"]}', headers={'User-Agent': useragent['useragent']}).text
            else:
                raise ValueError(ErrorList[0])
        else:
            raise ValueError(ErrorList[1])
    elif (type == 'booksByClass'):
        if ('schoolclass' in args and int(args.get("schoolclass")) <= 11):
            getGdzPage = requests.get(f'https://gdz.ru/class-{args["schoolclass"]}', headers={'User-Agent': useragent['useragent']}).text
        else:
            raise ValueError(ErrorList[1])
    elif (type == 'booksBySchoolItem'):
        if ('schoolitem' in args):
            getGdzPage = requests.get(f'https://gdz.ru/{args["schoolitem"]}', headers={'User-Agent': useragent['useragent']}).text
        else:
            raise ValueError(ErrorList[0])
    elif (type == 'popularBooks'):
        getGdzPage = requests.get(f'https://gdz.ru', headers={'User-Agent': useragent['useragent']}).text
    else:
        if (jsonEnable):
            return json.loads(json.dumps({"answers": []}))
        else:
            return {"answers": []}
    wrappedPage = bs4.BeautifulSoup(getGdzPage, 'lxml')
    for ul in wrappedPage.find_all(attrs={"class": "book-list"}):
        for li in ul.find_all("a", attrs={"class": ["book", "book-regular"]}):
            bookList.append({
                "url": {
                    "with_domain": f"https://gdz.ru{li['href']}",
                    "without_domain": li['href']
                },
                "name": str(li['title']).replace('ГДЗ ', ''),
                "authors": str(li.find('span', attrs={"itemprop": "author"}).string).split(','),
                "pubhouse": li.find('span', attrs={"itemprop": "publisher"}).string,
                "cover": "https:" + li.find("div", attrs={"class": "book-cover"}).select('noscript>img')[0]['src'],
            })                
    if (jsonEnable):
        return json.loads(json.dumps({"answers": bookList}))
    else:
        return {"answers": bookList}

    
def getTasksForBook(url, jsonEnable=True):
    # List
    answerList = {"answers": []}

    # UA
    useragent = ua.getRandomUserAgent()

    getGdzPage = requests.get(f"https://gdz.ru{url}", headers={'User-Agent': useragent['useragent']}).text
    wrappedPage = bs4.BeautifulSoup(getGdzPage, 'lxml')

    for sectionList in wrappedPage.find_all('section', attrs={'class': 'section-task'}):
        for header in sectionList.select('header>h2'):
            print(header.text.strip())