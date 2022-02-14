from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def mars_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, "html.parser")

    try:   
        slide_element = news_soup.select_one('div.list_text')
        news_title = news_title = slide_element.find("div", class_="content_title").get_text()
        news_para = slide_element.find("div", class_="article_teaser_body").get_text()
    
    except:
        print('value not found')
    return news_title, news_para

def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    full_image_button = browser.find_by_tag('button')[1]
    full_image_button.click()

    html = browser.html
    img_soup = soup(html, "html.parser")

    img_url = img_soup.find('img', class_='fancybox-image').get('src')
    return img_url

def mars_facts():
    url = 'https://galaxyfacts-mars.com/'

    try:
        mars_facts = pd.read_html('https://galaxyfacts-mars.com')[1]
        mars_facts.to_html('class=table table-striped')
    except: print('value not found')   
    
    return mars_facts

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_para = mars_news(browser)
    img_url = featured_image
    facts = mars_facts
    
    data = {
        "news_title": news_title,
        "news_para":news_para,
        "featured_image": featured_image(browser),
        "mars_facts": mars_facts()
    }

    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape_all())
