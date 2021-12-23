'''
[example]
    {
        title: 전지적 독자 시점
        description: (description),
        total_episode: 88,
        rating: 9.9,
        author: [슬리피-C, 싱숑, UMI],
        url: https://series.naver.com/comic/detail.series?productNo=5133669,
        img: (img)
    }
'''

from bs4 import BeautifulSoup
from requests import get
from requests import Response

from NaverSeries import search


def getInfo(id: int) -> dict:
    type = 'novel'
    try:
        url = f'https://series.naver.com/{type}/detail.series?productNo={str(id)}'
        response = get(url)
        if response.status_code == 200:
            return block(url, response, type)

        else:
            raise Exception('Requests Error! ' + str(response.status_code))
    except:
        try:
            type = 'comic'
            url = f'https://series.naver.com/{type}/detail.series?productNo={str(id)}'
            response = get(url)

            if response.status_code == 200:
                return block(url, response, type)

            else:
                raise Exception('Requests Error! ' + str(response.status_code))

        except:
            type = 'ebook'
            url = f'https://series.naver.com/{type}/detail.series?productNo={str(id)}'
            response = get(url)
            if response.status_code == 200:
                return block(url, response, type)

            else:
                raise Exception('Requests Error! ' + str(response.status_code))

def block(url:str, response:Response, type:str) -> dict:

    html = BeautifulSoup(response.text, 'html.parser')

    result = {'title': html.select_one('div.end_head h2').get_text().replace('\n', '').replace('\t', '')}

    if type == 'comic':
        description = html.find('div', {'class': 'end_dsc NE=a:cmi'}).select('div._synopsis')[1].get_text().replace(
            '\n', '').replace('\t', '').replace('\xa0', ' ').replace('\r', '\n')
        result['description'] = description[:len(description) - 2]

        result['img'] = html.find('div', {'class': 'aside NE=a:cmi'}).select_one('span.pic_area img')['src']

        result['total_episode'] = int(html.select_one('h5.end_total_episode strong').get_text())
        result['author'] = search(result['title'])['contents'][0]['author']

    elif type == 'novel':
        try:
            description = html.find('div', {'class': 'end_dsc NE=a:nvi'}).select(
                'div._synopsis')[1].get_text().replace('\n', '').replace('\t', '').replace('\xa0', ' ').replace('\r', '\n')
        except:
            description = html.find('div', {'class': 'end_dsc NE=a:nvi'}).select_one('div._synopsis').get_text().replace('\n', '').replace('\t', '').replace('\xa0', ' ').replace('\r', '\n')

        if description[len(description)-2:] == '접기':
            description = description[:len(description)-2]
        result['description'] = description


        try:
            result['img'] = html.find('div', {'class': 'aside NE=a:nvi'}).select_one('a.pic_area img')['src']
        except:
            result['img'] = html.find('div', {'class': 'aside NE=a:nvi'}).select_one('span.pic_area img')['src']
        result['total_episode'] = int(html.select_one('h5.end_total_episode strong').get_text())
        result['author'] = search(result['title'])['contents'][0]['author']

    elif type == 'ebook':
        description = html.find('div', {'class': 'end_dsc'}).select('div._synopsis')[1].get_text().replace(
            '\n', '').replace('\t', '').replace('\xa0', ' ').replace('\r', '\n')

        result['img'] = html.find('div', {'class': 'aside NE=a:ebi'}).select_one('a.pic_area img')['src']
        try:
            result['author'] = search(result['title'])['contents'][0]['author']
        except:
            result

    result['rating'] = float(html.select_one('div.end_head div.score_area em').get_text())
    result['url'] = url

    return result