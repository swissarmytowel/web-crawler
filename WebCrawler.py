from socket import error as socket_error
from urllib.error import URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup


class ParserError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)
        self.__message = "Parsing error occured"

    def what(self):
        return self.__message


class WebCrawler(object):
    """Class implementing web crawler.
       Crawls web pages for specific data retaining. """

    def __init__(self, url: str):
        # Init url and append 'https://' if absent
        self.__url = url
        if self.__url.count("https://") > 1:
            self.__url[8:].replace("https://", "")
        if not self.__url.startswith("https://"):
            self.__url = "https://" + self.__url

        self.__page_html = str()
        self.__retained_items_list = list()

        # Initialize connection, retrieve html page
        self.retrieve_html()
        self.__page_soup = BeautifulSoup(self.__page_html, "html.parser")

    def retrieve_html(self):
        """Retrieving page html-code by url"""
        try:
            url_client = urlopen(self.__url)
            self.__page_html = url_client.read()
            url_client.close()
        except URLError as e:
            print("Url error occurred: " + str(e.reason))
        except ValueError:
            print("Unknown url type: \'" + self.__url + "'")
        except socket_error as e:
            print("Socket error has occurred: " + e.errno + " in " + e.filename)

    def parse_html(self, tag: str):
        self.__retained_items_list = self.__page_soup.findAll(tag)
        if self.__retained_items_list is None:
            raise ParserError

    def get_retained_items(self):
        return self.__retained_items_list

if __name__ == "__main__":
    tmp = WebCrawler("https://www.python.org")
    try:
        tmp.parse_html(tag='img')
    except ParserError as e:
        print(e.what())
    print(len(tmp.get_retained_items()))

