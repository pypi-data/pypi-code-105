"""
Parser of everything from the Russian reshebnik GDZ.RU
"""

__version__ = "0.0.4"

import fake_useragent
import bs4
import requests


class GDZ:
    """Reshebnik object"""
    GDZ__URL = "https://gdz.ru"
    GDZ__RANDOM_USER_AGENT = fake_useragent.UserAgent()
    GDZ__SCHOOLITEMS = []

    class GDZObjects:
        class GDZ_GET:
            def GetBooksFromSite(url):
                getGdzPage = requests.get(GDZ.GDZ__URL + url,
                                          headers={
                                              'User-Agent':
                                              GDZ.GDZ__RANDOM_USER_AGENT.random
                                          }).text
                wrappedPage = bs4.BeautifulSoup(getGdzPage, 'lxml')
                bookList = []
                for ul in wrappedPage.find_all("ul",
                                               attrs={"class": "book-list"}):
                    for li in ul.find_all(
                            "a", attrs={"class": ["book", "book-regular"]}):
                        bookList.append(
                            GDZ.GDZObjects.GDZ_STUDENTBOOK(
                                url=li['href'],
                                bookname=str(li['title']).replace('ГДЗ ', ''),
                                authors=li.find('span',
                                                attrs={
                                                    "itemprop": "author"
                                                }).string,
                                pubhouse=li.find('span',
                                                 attrs={
                                                     "itemprop": "publisher"
                                                 }).string,
                                cover="https:" +
                                li.find("div", attrs={
                                    "class": "book-cover"
                                }).select('noscript>img')[0]['src']))
                return bookList
            
            def GetBookFromSite(url):
                pass

        class GDZ_ERRORS:
            class LargeNumberSchoolClass(Exception):
                def __init__(
                        self,
                        message="Number is greater than 11 or is not a number"
                ):
                    self.message = message
                    super().__init__(self.message)

            class NoConnectionToGDZ(Exception):
                def __init__(self, message="No connection to GDZ"):
                    self.message = message
                    super().__init__(self.message)

        class GDZ_STUDENTBOOK:
            """
            ### Contains textbook / workbook / study guide data
            """
            def __init__(self,
                         url,
                         bookname,
                         authors,
                         pubhouse,
                         cover=None) -> None:
                self.url = url
                self.cover = cover
                self.name = bookname
                self.authors = authors
                self.pubhouse = pubhouse

            def __repr__(self) -> str:
                return f"<{self.__class__.__name__} id={id(self)}>"

    class GDZGet:
        def schoolsubjects():
            """
            ### Allows you to get textbooks / workbooks / teaching aids (only by school subject)

            Subject name parsed from GDZ site, so run command and find your subject
            """
            return GDZ.GDZ__SCHOOLITEMS

        def books(schoolclass=8, schoolitem="all"):
            """
            ### Allows you to get textbooks / workbooks / teaching aids (there is a filter by class, academic subject)
            """
            if int(schoolclass) > 11:
                raise GDZ.GDZObjects.GDZ_ERRORS.LargeNumberSchoolClass
            else:
                if schoolitem == "all":
                    return GDZ.GDZObjects.GDZ_GET.GetBooksFromSite(
                        f'/class-{schoolclass}')
                else:
                    return GDZ.GDZObjects.GDZ_GET.GetBooksFromSite(
                        F'/class-{schoolclass}/{schoolitem}')

        def bookByClass(schoolclass=8):
            """
            ### Allows you to get textbooks / workbooks / teaching aids (only by class)
            """
            if int(schoolclass) > 11:
                raise GDZ.GDZObjects.GDZ_ERRORS.LargeNumberSchoolClass
            else:
                return GDZ.GDZObjects.GDZ_GET.GetBooksFromSite(
                    f'/class-{schoolclass}')

        def bookBySubject(schoolitem="algebra"):
            return GDZ.GDZObjects.GDZ_GET.GetBooksFromSite(f'/{schoolitem}')

        def bookInformation(gdz_studentbook):
            if type(gdz_studentbook) is GDZ.GDZObjects.GDZ_STUDENTBOOK:
                print('is a')
            else:
                print('str')

    def __init__(self) -> None:
        def getSchoolsItems():
            getGdzPage = requests.get(f"{self.GDZ__URL}",
                                      headers={
                                          'User-Agent':
                                          self.GDZ__RANDOM_USER_AGENT.random
                                      }).text
            wrappedPage = bs4.BeautifulSoup(getGdzPage, 'lxml')

            for schoolitem in wrappedPage.find_all(
                    'td', attrs={"class": "table-section-heading"}):
                ejectedUrl = schoolitem.find('a').get('href')
                self.GDZ__SCHOOLITEMS.append(str(ejectedUrl).replace('/', ''))

            try:
                self.GDZ__SCHOOLITEMS.pop(0)
            except IndexError:
                raise GDZ.GDZObjects.GDZ_ERRORS.NoConnectionToGDZ

        getSchoolsItems()