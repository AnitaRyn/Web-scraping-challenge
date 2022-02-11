
from splinter import Browser
from bs4 import BeautifulSoup as soup
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    data = {
        "news_title": news_title,
        "news_paragraph": news_para,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
        }
    browser.quit()

def mars_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, "html.parser")

    
    slide_elem = news_soup.select_one('div.list_text')
    news_title = slide_elem.find('div', class_='content_title')
    news_para = slide_elem.find('div', class_='article_teaser_body').get_text()

    return news_title, news_para

def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(2)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, "html.parser")

    img_url = img_soup.find('img', class_='fancybox-image').get('src')
    img_url = f'https://spaceimages-mars.com/{img_url}'
    return img_url

def mars_facts():
    url = 'https://galaxyfacts-mars.com/'

    df = pd.read_html('https://galaxyfacts-mars.com')[1]
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    for x in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item img')[x].click()
        sample_element = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_element['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    hemi_soup = soup(html_text, "html.parser")
    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres


if __name__ == "__main__":

   
    print(scrape_all())

