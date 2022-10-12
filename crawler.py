import bs4
import requests
from datetime import datetime
import time


def get_page_content(url):
    page = requests.get(url, verify=False, headers={"Accept-Language": "en-US"})
    return bs4.BeautifulSoup(page.content, "html.parser")


def crawler_tradingview(url, type):
    html = get_page_content(url)

    title = html.find('h1', class_='tv-chart-view__title-name js-chart-view__name').text.strip()
    description = html.find('div', class_='tv-chart-view__description-wrap js-chart-view__description').text
    posted_date = datetime.fromtimestamp(float(html.find('span', class_='tv-chart-view__title-time')['data-timestamp']))

    if type == 'text':
        pass
        # with open("media/text_file.txt", "w", encoding = 'utf-8') as file:
        #     file.write(title)
        #     file.write(description)
    else:
        html.find('div', class_='tv-header tv-header__top js-site-header-container tv-header--sticky').decompose()
        html.find('div', class_='tv-chart-view__disclaimer-wrapper').decompose()
        html.find('div', class_='tv-chart-view__signature').decompose()
        html.find('div', class_='tv-chart-view__social-links').decompose()
        html.find('div', class_='js-chart-view__linked-charts').decompose()
        html.find('div', class_='tv-comment-tree').decompose()
        html.find('footer', class_='tv-footer js-footer').decompose()
        
        # with open("media/html_file.html", "w", encoding = 'utf-8') as file:
        #     file.write(str(html.prettify()))
            
        description = str(html.prettify())

    return {
        'title': title,
        'content': description,
        'posted_date': posted_date
    }


def crawler_investing(url, type):
    html = get_page_content(url)

    title = html.find('h1', class_='articleHeader').text.strip()

    div_time = html.find('div', class_='contentSectionDetails')
    posted_date = div_time.find('span').text.split('(')[1].strip(")")

    html.find('header').decompose()
    html.find('aside').decompose()
    html.find('footer').decompose()
    html.find('h2').decompose()
    html.find('div', class_='contentSectionDetails').decompose()
    html.find('div', class_='articleControl withSave').decompose()
    html.find('div', class_='imgCarousel').decompose()
    html.find('div', class_='midHeader').decompose()
    html.find('div', class_='slider').decompose()
    html.find('div', class_='articleFooter').decompose()
    html.find('div', class_='largeTitle').decompose()
    html.find('div', class_='signupWrap js-gen-popup displayNone').decompose()
    html.find('div', class_='addAComment js-main-comment').decompose()
    html.find('div', class_='doubleLineSeperator').decompose()
    
    description = html.find('div', class_='WYSIWYG articlePage').text
    
    if type == 'text':
        pass
        # with open("media/text_file.txt", "w", encoding = 'utf-8') as file:
        #     file.write(title)
        #     file.write(description)
    else:
        for s in html.select('script'):
            s.extract()

        # with open("media/html_file.html", "w", encoding = 'utf-8') as file:
        #     file.write(str(html.prettify()))
            
        description = str(html.prettify())

    return {
        'title': title,
        'content': description,
        'posted_date': posted_date
    }