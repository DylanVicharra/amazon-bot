from . import BeautifulSoup
from ..constant import AMAZON_URL, ASIN_URL

class AmazonSearch:
    def __init__(self, sourcePage):
        self._search = BeautifulSoup(sourcePage.page_source, 'html.parser', multi_valued_attributes=None)
        self._searchResult = self.searchResult()

    def searchResult(self):
        productSearch = self._search.find_all(lambda tag:(tag.name=="div") and ('s-asin' in str(tag.get('class'))))
        if productSearch is not None and productSearch:
            result = list(map(lambda link: str(link.get('data-asin')).strip(), productSearch))
            return result 
        return productSearch

    def firstProductSearch(self):
        if self._searchResult and self._searchResult is not None:
            return ASIN_URL.format(AMAZON_URL, self._searchResult[0])
        return None