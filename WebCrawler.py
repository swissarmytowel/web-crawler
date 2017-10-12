from socket import error as socket_error
from urllib.error import URLError
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup


class ParserError(Exception):
    """Custom HTML parser exception"""
    def __init__(self, message=None):
        Exception.__init__(self)
        if message is not None:
            self.__message = message
        else:
            self.__message = "Parsing html error occurred"

    @property
    def what(self):
        return self.__message


class WebCrawler(object):
    """Class implementing web crawler.
       Crawls web pages for specific data retaining. """
    def __init__(self, url: str):
        """
        WebCrawler constructor
        :param url: address of web page to be crawled
        """
        # Initialize url and append 'https://' if absent
        self.__url = url
        if self.__url.count("https://") > 1:
            self.__url[8:].replace("https://", "")
        if not self.__url.startswith("https://"):
            self.__url = "https://" + self.__url

        # Initialize connection, retrieve html page
        self.__page_html = str()
        self.__retained_items_list = list()
        self.retrieve_html()
        self.__page_soup = BeautifulSoup(self.__page_html, "html.parser")

    def retrieve_html(self):
        """Retrieving page html-code by url"""
        try:
            url_client = urlopen(self.__url)
            self.__page_html = url_client.read()
            url_client.close()
        except URLError as url_exception:
            print("Url error occurred: " + str(url_exception.reason))
        except ValueError:
            print("Unknown url type: \'" + self.__url + "'")
        except socket_error as socket_exception:
            print("Socket error has occurred: " + socket_exception.errno + " in " + socket_exception.filename)

    def parse_html(self, tag: str, sub_tag: str = None):
        """
        Parses HTML for tag occurrences and then gets substring by sub tag
        :param tag: tag for initial splitting
        :param sub_tag: sub tag for retrieving parts of interest
        """
        self.__retained_items_list = self.__page_soup.findAll(tag)
        if self.__retained_items_list is None:
            raise ParserError
        # Retrieve part of interest, if :param sub_tag was specified
        if sub_tag is not None:
            self.__retained_items_list = [item.get(sub_tag)
                                          if item.get(sub_tag).startswith(self.__url)
                                          else urljoin(self.__url, item.get(sub_tag))
                                          for item in self.__retained_items_list]

    @property
    def get_retained_items(self) -> list:
        return self.__retained_items_list


if __name__ == "__main__":

    # Use case

    test_url = "python.org"
    test_tag = "img"
    test_sub_tag = 'src'
    test_spider = WebCrawler(test_url)
    try:
        test_spider.parse_html(test_tag, test_sub_tag)
    except ParserError as e:
        print(e.what)

    print("Found " + str(len(test_spider.get_retained_items)) + " items from \"" + test_url +
          "\" by tag \"" + test_tag + "\"")
    print("\n".join(test_spider.get_retained_items))
