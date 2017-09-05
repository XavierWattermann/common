# common
## Description
common.py is a list of frequently used Python functions, such as reading/writing to a file, creating folders, etc.

## Functions:

### create_driver()
Creates a webdriver using a ChromeDriver or PhantomJS.
##### Dependices
 - [selenium](http://www.seleniumhq.org/)
 - [PhantomJS](http://phantomjs.org/)
 - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
 
### get_soup(url)
Creates a BeautifulSoup object, given a passed url.
##### Parameters
url - the url to be parsed. 
##### Dependices
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

### find_all(soup, first, second, third)
A wrapper for BeautifulSoup.find_all(first: {second: third})
##### Parameters
soup - A BeautifulSoup Object

first, second, third - items to search for
##### Dependices
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
