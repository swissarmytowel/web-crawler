from bs4 import BeautifulSoup
from socket import error as SocketError
from urllib.error import URLError
from urllib.request import urlopen


class WebCrawler(object):
    """Class implementing web crawler.
       Crawls web pages for specific data retaining. """

    __page_html = ""

    def __init__(self, url: str):
        # Init url and append 'https://' if absent
        self.__url = url
        if self.__url[:7] != "https://":
            self.__url = "https://" + self.__url
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
            print("Url error occurred: " + e.reason())
        except ValueError:
            print("Unknown url type: \'" + self.__url + "'")
        except SocketError as e:
            print("Socket error has occurred: " + e.errno + " in " + e.filename)

if __file__ == "__main__":
    c = WebCrawler("stackoverflow.com")




