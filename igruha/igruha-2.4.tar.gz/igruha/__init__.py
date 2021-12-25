from requests import session as Sess
from bs4 import BeautifulSoup
import cfscrape


class Igruha:
    def __init__(self, session=Sess(), url='https://q.itorrents-igruha.org/', headers=None):
        if headers is None:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                          'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, utf-8',
                'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
            }
        self.url = url
        self.session = cfscrape.create_scraper(sess=session)
        self.headers = headers
        self.data = {
            'do': 'search',
            'subaction': 'search',
            'story': '',
        }
        self.data2 = {
            'do': 'search',
            'subaction': 'search',
            'search_start': 2,
            'full_search': 0,
            'story': '',
        }
        self.lastgame = None

    def search(self, gamez):
        self.lastgame = gamez
        self.data['story'] = gamez
        self.data2['story'] = gamez
        responses = []
        response = self.session.post(url=self.url, data=self.data, headers=self.headers)
        if 'поиск по сайту не дал никаких результатов' in response.text:
            return None
        responses.append(response)
        tree = BeautifulSoup(response.text, 'lxml')
        try:
            lens = int(tree.find_all('a', {'onclick': "javascript:list_submit("}, partial=True)[-1].text)
            for i in range(2, lens + 1):
                responses.append(self.session.post(url=self.url, data=self.data2, headers=self.headers))
                self.data2['search_start'] += 1
        except: pass
        self.data2['search_start'] = 2
        self.result = AllResult([Result(response.text, self.session) for response in responses])
        return self.result

    def main_games(self):
        url = 'http://q.itorrents-igruha.org/'
        h = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, utf-8',
            'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'cookie': 'cf_clearance=y9zIS75pSnpeSGbX0ZAOw5yVk7Ihi33kBqmb7rEmWmw-1640203407-0-150; PHPSESSID=2duinfc5nr5mve71sfdu1f23l0; __cf_bm=7aVPWkpFwFf2uHwaokFTcK3M_joPgBSLtL1E9K8fyDY-1640445672-0-ATLfN/EX+wRTM5pmqgfM+r5D8SvXKyDZv7bvtjbbCzTbGIob784Bv7vEZl+B9B/JGEL+SZjRNToPKClZ4PgMpSdkO6r+amzfaINCYAVg9KLUsAt3AWbm9wVmuYoeYya4DQ==',
            'referer': 'https://www.google.com/',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
             }
        resp = self.session.get(url, headers=h).text
        self.session.headers = self.headers
        return Result(resp, self.session, 'main')

    def get_lastgame(self):
        return self.lastgame

    def get_session(self):
        return self.session


class Game:
    def __init__(self, source, session):
        self.source = source
        self.session = session
        self.name = self.source.find('img', {'class': 'article-img'}).get('alt')
        self.link = self.source.find('a').get('href')
        self.img = self.source.find('img', {'class': 'article-img'}).get('src')

        self.released = None
        self.genre = None
        self.developer = None
        self.publisher = None
        self.platform = None
        self.edition_type = None
        self.lang_interface = None
        self.lang_voice = None
        self.tablet = None
        self.requirements = None
        self.description = None
        self.trailer = None
        self.screenshots = None
        self.id = None
        self.torrent = 'https://q.itorrents-igruha.org/engine/download.php?id='+str(self.id)

    def get_details(self):
        text = self.session.post(url=self.link).text
        tree = BeautifulSoup(text, "lxml").find('div', {'id': "dle-content"})
        self.alls = tree.find('div', {'style': 'padding-left: 215px;'}).text.replace('<br>', "\n")
        alls = '\n'.join(tree.find('div', {'style': "padding-left: 215px;"}).text.split('<br>'))
        try: self.released = alls.split('Год выпуска: ')[1].split('Жанр')[0]
        except:
            try: self.released = alls.split('Дата выхода: ')[1].split('Жанр')[0]
            except: pass
        try: self.genre = alls.split('Жанр: ')[1].split('Разработчик')[0]
        except: pass
        try: self.developer = alls.split('Разработчик: ')[1].split('Издательство')[0]
        except: pass
        try: self.publisher = alls.split('Издательство: ')[1].split('Платформа')[0]
        except: self.publisher = alls.split('Издатель: ')[1].split('Платформа')[0]
        try: self.platform = alls.split('Платформа: ')[1].split('Тип')[0]
        except: pass
        try: self.edition_type = alls.split('Тип издания: ')[1].split('интерфейса')[0]
        except: pass
        try: self.lang_interface = alls.split('интерфейса: ')[1].split('озвучки: ')[0]
        except: pass
        try: self.lang_voice = alls.split('озвучки: ')[1].split('Таблетка')[0]
        except: pass
        try: self.tablet = alls.split('летка:')[1].split('Сист')[0]
        except: print('WARN: Не удалось найти информацию про таблетку')
        try: self.requirements = self.alls.split('Системные требования:')[1].split('\n\n')[0]
        except: pass
        try: self.description = tree.find('div', {'class': 'blockinfo'}).text.split('h2')[0].replace('<br>', '\n').\
            replace('<ul>', '• ').replace('</ul>', '\n')
        except: pass

        try: self.trailer = 'https://youtu.be/'+tree.find('div', {'class': 'youtube'}).get('id')
        except: pass

        self.ids = [i.get('href').split('id=')[1] for i in tree.find_all('a', {'class': 'torrent'})]
        self.torrents = []

        x = tree.find_all('span', {'style': 'font-size:14pt;'})
        self.torrent_names = [i.find('span', {'style': 'color: #89c80e;'}).text for i in x if i.find('span', {'style': 'color: #89c80e;'}) is not None]

        for i in enumerate(tree.find_all('a', {'class': 'torrent'})):
            self.torrents.append(Torrent(i[1], self.torrent_names[i[0]], self.session, self.name))

        self.id = self.ids[0]
        self.torrent = 'https://q.itorrents-igruha.org/engine/download.php?id=' + str(self.id)
        return self

    def to_dict(self):
        return self.__dict__

    def download(self, name=None):
        if name is None:
            name = self.name
        response = self.session.get(self.torrent).content
        file = open('%s.torrent' % name, 'wb')
        file.write(response)
        return file


class Torrent:
    def __init__(self, source, name, session, game_name):
        self.source = source
        self.session = session
        self.link = 'https://q.itorrents-igruha.org/engine/download.php?id=' + self.source.get('href').split('id=')[1]
        self.name = name
        self.game_name = game_name

    def download(self, name=None):
        if name is None:
            name = self.game_name
        response = self.session.get(self.link).content
        file = open('%s.torrent' % name, 'wb')
        file.write(response)
        return file


class Result:
    def __init__(self, source: str = '', session: Sess = Sess(), type: str = 'find'):
        self.source = source
        self.session = session

        self.tree = BeautifulSoup(self.source, "lxml")
        self.type = type
        if self.type == 'main':
            self.game_list = self.tree.find('div', {'class': 'global-container'})
            if self.game_list is None:
                raise Exception('Cloudflare не пропускает вас!')
            self.games_source = self.game_list.find_all('div', {'class': 'article-film'})
        else:
            self.game_list = self.tree.find('div', {'id': 'dle-content'})
            self.len = int(self.source.split('найдено ')[1].split(' ответов')[0])
            if self.game_list is None:
                raise Exception('Cloudflare не пропускает вас!')
            self.games_source = self.game_list.find_all('div', {'class': 'article-film1'})
        self.games = [Game(i, self.session) for i in self.games_source]


class AllResult:
    def __init__(self, array):
        self.array = array
        self.games = []
        for i in self.array:
            self.games += i.games



'''parser = Igruha()
print(parser.main_games().games[0].name)
print(len(parser.search('call').games))
game = parser.search('Far Cry').games[0]
details = game.get_details()
game.torrents[0].download()'''

