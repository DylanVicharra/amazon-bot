import setuptools

setuptools.setup(
    name='amazon-bot', 
    version='1.0',
    author='Dylan Vicharra',
    description='Web Scraping de productos de Amazon con Selenium y BeautifulSoup',
    packages=setuptools.find_packages(),
    install_requires=['beautifulsoup4','selenium','webdriver-manager','pandas','pathlib'],
    python_requires='>=3.6.5',
    entry_points={  
        "console_scripts": [
            "extract_product_list=extract_product_list.__main__:main",
        ],
    },
)

