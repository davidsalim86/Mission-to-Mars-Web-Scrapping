# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}

    # NASA Mars News

    # visit url1
    browser = Browser('chrome', **executable_path, headless=False)
    url1 = "https://redplanetscience.com/"
    browser.visit(url1)
    # wait for 2 seconds
    time.sleep(2)
    # html object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # collect data
    news = soup.find('div', class_='list_text')
    news_title = news.find('div', class_='content_title').text
    news_p = news.find('div', class_='article_teaser_body').text
    # quit url1
    browser.quit()

    # JPL Mars Space Images - Featured Image

    # visit url2
    browser = Browser('chrome', **executable_path, headless=False)
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    # wait for 2 seconds
    time.sleep(2)
    # html object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain list_text
    image = soup.find_all('div', class_="floating_text_area")
    # collecting image url
    image_url = []
    featured_image_url = []
    for x in image:
        link = x.find('a')['href']
        image_url.append(link)
    featured_image_url = [url2 + url for url in image_url]
    # quit url2
    browser.quit()

    # Mars Facts

    # use panda read url3
    url3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url3)
    # collecting and cleaning data
    table_df = tables[1]
    table_df.columns = ['Description','Mars']
    table_df = table_df.replace({'Orbit Distance:':'Distance from Sun:', 'Orbit Period:':'Length of Year:'})
    table_html = table_df.to_html(index=False, escape=True, justify="left", col_space=10)

    # Mars Hemispheres

    # visit url4
    browser = Browser('chrome', **executable_path, headless=False)
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)
    # wait for 2 seconds
    time.sleep(2)
    # html object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain item
    item = soup.find_all('div', class_="item")
    # collecting title
    title_list= []
    for x in item:
        text = x.find('h3')
        title_list.append(text.text)
    # collecting image urls
    image_url2 = []
    complete_image_url2 = []
    for x in range(4):
        time.sleep(2)
        browser.links.find_by_partial_text(title_list[x]).click()
        # html object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        # collect links
        downloads = soup.find('img', class_='wide-image')['src']
        image_url2.append(downloads)
        browser.links.find_by_partial_text('Back').click()
    complete_image_url2 = [url4 + url for url in image_url2]
    # quit url4
    browser.quit()
    
    hemisphere_image_urls = []
    for i, j in zip(title_list, complete_image_url2):
        hemisphere_image_urls.append({"title": i, "img_url":j})
    
    scrape_data_dict = dict({'news_title':news_title,'news_p':news_p,'featured_image_url':featured_image_url,'table_html':table_html,'hemisphere_image_url':hemisphere_image_urls})
    
    return scrape_data_dict