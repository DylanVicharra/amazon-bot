import sys
from .models import AmazonProduct, AmazonSearch
from .file_manager import *
from .webdriver import driverChrome
from .constant import *
from .errors import ExcelFileNoFound

def getAmazonProducts(amazonOverallList):
    listAsinProducts = readExcelFile(str(getExcelFile(TRACKER_PATH)))
    print(f'Se extraerá información de {len(listAsinProducts)} productos.')
    for product in listAsinProducts:
        if len(product)==10 or (product in 'https://www'):   
            driverChrome.get(ASIN_URL.format(AMAZON_URL,product.strip()))
            addAmazonProduct = AmazonProduct(driverChrome)
            amazonOverallList.append(addAmazonProduct)
            amazonOverallList.extend(getAmazonProductVariants(addAmazonProduct))
        else:
            driverChrome.get(SEARCH_PRODUCT_URL.format(AMAZON_URL,product.replace(" ","+").strip()))
            amazonSearch = AmazonSearch(driverChrome)
            urlProduct = amazonSearch.firstProductSearch()
            if urlProduct is not None:
                driverChrome.get(urlProduct)
                addAmazonProduct = AmazonProduct(driverChrome)
                amazonOverallList.append(addAmazonProduct)
                amazonOverallList.extend(getAmazonProductVariants(addAmazonProduct))
    return amazonOverallList

def getAmazonProductVariants(amazonProduct):
    productVariants = []
    variantsUrl = amazonProduct.getVariants(driverChrome)
    if variantsUrl is not None:
        for url in variantsUrl:
            driverChrome.get(url)
            productVariants.append(AmazonProduct(driverChrome))
        return productVariants
    return productVariants

def main():
    try:
        print('Inicializando extracción de información de productos Amazon... ')
        # Instance list of amazon products
        amazonOverallList = []
        # Instance file excel        
        amazonSearchExcel = createExcelFile()

        amazonOverallList = getAmazonProducts(amazonOverallList)
        
        print(f'Cantidad total de productos obtenidos: {len(amazonOverallList)}')
        for product in amazonOverallList:
            writeExcelFile(amazonSearchExcel, product)

        saveExcelFile(amazonSearchExcel, SEARCH_PATH)
        print('Se creo un archivo excel con los datos obtenidos.')
        del amazonOverallList 
        driverChrome.quit()
        print('Finalizando programa...')
    except Exception as ex:
        print(f'{ex.__class__.__name__}: {ex}')
        print('Ha ocurrrido un error inesperado.')
        print(f'Cantidad total de productos obtenidos: {len(amazonOverallList)}.\nSe creo un archivo excel con los datos obtenidos hasta el momento.\nFinalizando programa...')
        for product in amazonOverallList:
            writeExcelFile(amazonSearchExcel, product)
        saveExcelFile(amazonSearchExcel, SEARCH_PATH)
        del amazonOverallList
        driverChrome.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()

