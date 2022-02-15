from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#Set up Splinter for all scraped data, store into dictionary
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_para = mars_news(browser)
    
    data = {
        "news_title": news_title,
        "news_para":news_para,
        "featured_image": featured_image(browser),
        "mars_facts": mars_facts()
    }
    #close the browser after scraping and retunr results
    browser.quit()
    return data
#Scrape news title and paragraph
def mars_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, "html.parser")
    
    # Add try/except for error handling
    try:   
        slide_element = news_soup.select_one('div.list_text')
        news_title = slide_element.find("div", class_="content_title").get_text()
        news_para = slide_element.find("div", class_="article_teaser_body").get_text()
    
    except:
        print('value not found')
    return news_title, news_para
#Scrape the image
def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    full_image_button = browser.find_by_tag('button')[1]
    full_image_button.click()

    html = browser.html
    img_soup = soup(html, "html.parser")

    img_url = img_soup.find('img', class_='fancybox-image').get('src')
    return img_url
    
#Scrape the facts table
def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap element
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    print(scrape_all())
