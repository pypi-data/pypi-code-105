'''
[example]
    {
        contents:
        {
            0:
            [
                {title: 전지적 독자 시점 (총 551화/미완결), id: (id), author: [싱숑] },
                ...
            ],

            1:
            [
                {title: 전지적 독자 시점 [독점] (총 88화/미완결), id: (id), author: [슬리피-C, 싱숑, UMI] },
                ...
            ],

            2:
            [
                ...
            ]
        }
    }
'''

from bs4 import BeautifulSoup
from requests import get

def search(keyword:str, focus:str='novel') -> dict:
    #Request
    url = f'https://series.naver.com/search/search.series?fs={focus}&q={keyword}'
    response = get(url)

    if response.status_code == 200:

        html = BeautifulSoup(response.text, 'html.parser')
        search_data = html.find('div', {'class': 'com_srch'}).select('div.bs')


        if(len(search_data) > 0):

            result = {
                'contents': []
            }

            for elem1 in search_data:
                books = elem1.select('li')

                for elem2 in books:
                    book = {}
                    book_info = elem2.select_one('div.cont')

                    book['title'] = book_info.select_one('h3').get_text().replace('\n', '').replace('\t', '')
                    book['id'] = replaceUnusingTextInProducNo(book_info.select_one('h3 a')['href'])

                    try:
                        book['author'] = list(map(lambda x : x.replace(' ', '') , book_info.select_one('p.info span.ellipsis').get_text().split(',')))
                    except:
                        book['author'] = [book_info.select_one('p.info').get_text().split('\n')[5].replace('|', '')[1:]]

                    if not result['contents'].__contains__(book):
                        result['contents'].append(book)

            return result

        else:
            raise Exception("Cannot found book!")

    else:
        raise Exception('Error occurred while request! error: ' + str(response.status_code))

def replaceUnusingTextInProducNo(product:str) -> int:
    if product.__contains__('/novel/detail.series?productNo='):
        return int(product.replace('/novel/detail.series?productNo=', ''))

    elif product.__contains__('/comic/detail.series?productNo='):
        return int(product.replace('/comic/detail.series?productNo=', ''))

    elif product.__contains__('/ebook/detail.series?productNo='):
        return int(product.replace('/ebook/detail.series?productNo=', ''))

    else:
        return product