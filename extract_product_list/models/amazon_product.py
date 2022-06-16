import itertools
from time import sleep
from . import BeautifulSoup

class AmazonProduct:
    # source page is a webdriver instance
    def __init__(self, sourcePage):
        self._url = sourcePage.current_url
        self._productPage = BeautifulSoup(sourcePage.page_source, 'html.parser', multi_valued_attributes=None)
        self._variants = self.variantsCombination()
    
    def __str__(self):
        return "AmazonProduct[name: {}, price: {}, availability: {}, url: {}]".format(self.getName, self.getPrice, self.getAvailability, self.getUrl)
            
    @property
    def getPrice(self):    
        detailsProduct = self._productPage.find(lambda tag:(tag.name=="div") and ('container_horizontal_center' in str(tag.get('class')) or 'centerCol' in str(tag.get('id'))))
        detailPrice = detailsProduct.find(lambda tag:(tag.name=="span") and ('PriceToPay' in str(tag.get('class'))))

        if (detailPrice is not None) and (detailPrice.children):
            return detailPrice.findChild("span").text.strip()
        elif detailPrice: 
            return detailPrice.text.strip()
        else: 
            return ""    

    @property 
    def getUrl(self):
        return self._url

    @property
    def getAvailability(self):
        detailAvailability = self._productPage.find(lambda tag:(tag.name=="div") and ('feature_Availability celwidget' in str(tag.get('class')) or 'availability' in str(tag.get('id'))))
        if detailAvailability is not None:
            return detailAvailability.text.replace("    ","").strip()
        return detailAvailability

    @property 
    def getName(self):
        detailName = self._productPage.find('span',{'id':"productTitle"})
        if detailName is not None:
            return detailName.text.strip()
        return detailName

    @property
    def getDescription(self):
        detailsDescription = self._productPage.find(lambda tag:(tag.name=="div") and ('Twister' in str(tag.get('class'))))
        if detailsDescription is not None: 
            productDescription = detailsDescription.find_all('div',{'class':'a-row'})
            descriptionText = " ".join(map(lambda tag: str(tag.text.replace('\n'," ").replace('          ',' ').strip()),productDescription))
            return descriptionText 
        return None

    def searchSectionVariants(self):
        detailsVariants = self._productPage.find(lambda tag:(tag.name=="div") and ('Twister' in str(tag.get('class'))))
        variantsSectionList = []
        if detailsVariants is not None:
            variantsSection = detailsVariants.find_all("ul")
            if (variantsSection is not None) and (variantsSection):
                for i in variantsSection:
                    valuesVariants = i.find_all('li')
                    variantsSectionList.append(valuesVariants)
                return variantsSectionList
            else:
                return detailsVariants
        else:
            return detailsVariants
    
    def variantsCombination(self):
        variantsSection = self.searchSectionVariants()
        variantCombination = []

        if (variantsSection is not None) and (variantsSection): 
            for combinations in itertools.product(*variantsSection):
                variantCombination.append(list(combinations))

            return variantCombination
        else:
            return None
   
    def getVariants(self, driver):
        variantsUrl=[]
        #driver.get(self._url)

        if self._variants is not None:
            for combinationButton in self._variants:
                for j in combinationButton:
                    titleElement = j.get('title')
                    webElement = driver.find_element_by_xpath(f'//li[@title="{titleElement}"]')
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", webElement)
                    webElement.click()
                    sleep(2)
                sleep(3)
                urlPage = str(driver.current_url)
                if self._url in urlPage:
                    pass
                else:
                    variantsUrl.append(urlPage)
            return variantsUrl
        else:
            return None
        