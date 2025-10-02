from chemdataextractor.scrape.pub.rsc import RscSearchScraper
from os.path import join, exists
from os import mkdir, listdir
from selenium import webdriver

import requests

RSC_FilePath = r'' # output path
Query = '' # query
start_page = 0
noOfPages = 98

FilePath = join(RSC_FilePath, Query)


def queryScrapeRSC(no_of_pages=noOfPages, query=Query):
    article_list = []
    Driver = webdriver.Chrome()  # Initialise web driver
    for page in range(0, no_of_pages):  # Scrape RSC web pages for article information (24 articles per page)
        scrape = RscSearchScraper(driver=Driver).run(query, page=page+start_page)
        articles = scrape.serialize()  # Compile scraped article information
        for article in articles:
            print(article["doi"])
            article_list.append(article)
    return article_list


def getHTML(articles, filePath=FilePath):
    alreadyScraped = listdir(filePath)
    if not exists(FilePath):    # Check if output dir exists; create if not
        mkdir(FilePath)
    Driver = webdriver.Chrome()     # Initialise web driver
    for article in articles:    # Sequentially go through each URLs from scraped article information
        doi = article['doi']
        doi = doi.replace('/', '..')
        path = join(filePath, doi + '.html')   # Create file path
        if doi + '.html' not in alreadyScraped:
            try:
                Driver.get(article['html_url'])
                art = Driver.page_source    # Download article .html
                art = art.encode()
                with open(path, 'wb') as HTML_File:     # Save article .html to file
                    HTML_File.write(art)
            except:
                KeyError


articles = queryScrapeRSC()
getHTML(articles)


