# Import modules
# ------------------------------------------------------------

from bs4 import BeautifulSoup as soup
from splinter import Browser

# Set up functions
# ------------------------------------------------------------

def getParsedWebpage(browser, url):
    """
    Initializes Splinter Browser and returns a BeautifulSoup-parsed (HTML) ResultSet.
    """
    browser.visit(url)
    html = browser.html
    webpage = soup(html, 'html.parser')
    
    return webpage;


def getParsedTextList(resultSet):
    """
    This function takes in a BeautifulSoup ResultSet and returns
    a list. Warning: Parses using get_text()! So if you want to
    parse each Result to get Text in a List, this is for you.
    """
    
    result_list = []
    
    for result in resultSet:
        result_list.append(result.get_text())
        
    return result_list;

hidden_urls = ['https://mars.nasa.gov/news/',
              'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit',
              'https://twitter.com/marswxreport?lang=en',
              'https://space-facts.com/mars/',
              'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars']    