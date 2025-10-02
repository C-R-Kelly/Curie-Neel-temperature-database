from elsevier_scraper import *
from os.path import join, exists
from os import makedirs
import random

Elsevier_FilePath = '' # output path
queryText = '' # search query
Date = 2021 # year
Query = {'qs': queryText, 'date': f'{Date}'}

FilePath = join(Elsevier_FilePath, queryText)

api_key = '' # api key
PaperNo = 0
downloadLimit = 300


def queryScrapeElsevier(APIKey=api_key, query=Query, paperNo=PaperNo, date=Date, filePath=FilePath):
    scraper = ElsevierScraper(key=APIKey)    # Initialise scraper
    if not exists(filePath):    # check if output directory exists; create it if not
        makedirs(filePath)
    path = join(filePath, str(date) + '.txt')   # create file path that will contain URL list
    scraper.query(query, save_file=path, max_papers=paperNo)    # Query Elsevier and save relevant URLs to file
    return path


def getXML(APIKey=api_key, date=Date, filePath=FilePath, journal=False):
    scraper = ElsevierScraper(key=APIKey)   # Initialise Scraper
    ScrapedArticles = os.listdir(filePath)  # Obtain list of articles already downloaded
    if journal:
        articleList = join(filePath, 'dois.txt')
    else:
        articleList = join(filePath, str(date) + '.txt')    # file path for URL list

    with open(articleList) as articleListFile:  # Open URL list
        counter = 0
        for article in articleListFile:  # Sequentially scrape articles from URL list, save as .xml
            url = article[:-1]
            fileName = url.split('/')[-1] + '.xml'
            if fileName not in ScrapedArticles: # Skip already downloaded articles
                scraper.save_xml_from_doi(url, filePath + '\\')
                counter += 1
                if counter >= downloadLimit:  # End download sequence if download limit reached
                    break

p = queryScrapeElsevier() # save doi's
getXML() # scrape papers