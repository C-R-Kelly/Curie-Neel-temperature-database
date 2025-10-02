# -*- coding: utf-8 -*-
"""
elsevier_scraper.py
Scraper for the Elsevier webpages using the Elsevier developer API
by Callum Court (https://github.com/cjcourt)

"""
import requests
import os
import xml.etree.ElementTree as ET
import codecs
from bs4 import BeautifulSoup
import time
import sys
import json


# ElsevierScraper class by Callumn Court
class ElsevierScraper:
    """ Scraper for getting the results of a search on the Elsevier API"""

    def __init__(self, key):
        self.dois = []
        self.urls = []
        self.titles = None
        self.journal_list = None
        self.num_of_articles = 0
        self.key = key
        self.elsevier_max_show_value = 100

    def save_xml(self, url, save_directory, max_retries=5):
        """
        Save an article xml from url
        :param url: Url to XML file
        :param save_directory: Where to save the article
        :param max_retries: Number of failed attempts before giving up
        :return:
        """
        if not os.path.isdir(save_directory):
            os.mkdir(save_directory)

        # Keep trying in case we fail
        succeeded = False
        attempts = 0
        try:
            while not succeeded:
                r = requests.get(
                    url + '?view=FULL', headers={'X-ELS-APIKey': self.key}, timeout=400)
                print(r.url + '&APIKey=' + self.key)
                if 'REQUESTOR_NOT_ENTITLED' in r.text or 'RESOURCE_NOT_FOUND' in r.text:
                    print("Trying again")
                    attempts += 1
                    if attempts >= max_retries:
                        succeeded = True
                        print("Moving on")
                        continue
                elif '<service-error>' in r.text:
                    print("Not entitled")
                    succeeded = True
                    continue
                else:
                    succeeded = True
                    soup = BeautifulSoup(r.text, "lxml")
                    doi = soup.find('xocs:doi').text.split('/')[-1]
                    file_name = save_directory + doi + '.xml'
                    paper_file = codecs.open(file_name, 'w', encoding='utf8')
                    print(r.text, file=paper_file)
                    paper_file.close()
                    # print("Paper downloaded.")

        except requests.exceptions.Timeout as e:
            print(e)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        except ET.ParseError as e:
            print(e)
        return

    def save_xml_from_doi(self, doi, save_directory, max_retries=5):
        """
        Save an article xml from url
        :param url: Url to XML file
        :param save_directory: Where to save the article
        :param max_retries: Number of failed attempts before giving up
        :return:
        """
        if not os.path.isdir(save_directory):
            os.mkdir(save_directory)

        # Keep trying in case we fail
        succeeded = False
        attempts = 0
        try:
            while not succeeded:
                r = requests.get(
                    "https://api.elsevier.com/content/article/doi/" + doi + '?view=FULL', headers={'X-ELS-APIKey': self.key}, timeout=400)
                # print(r.url + '&APIKey=' + self.key)
                if 'REQUESTOR_NOT_ENTITLED' in r.text or 'RESOURCE_NOT_FOUND' in r.text:
                    print("Trying again")
                    attempts += 1
                    if attempts >= max_retries:
                        succeeded = True
                        print("Moving on")
                        continue
                elif '<service-error>' in r.text:
                    print("Not entitled")
                    succeeded = True
                    continue
                else:
                    succeeded = True
                    soup = BeautifulSoup(r.text, "lxml")
                    doi = soup.find('xocs:doi').text.split('/')[-1]
                    file_name = save_directory + doi + '.xml'
                    paper_file = codecs.open(file_name, 'w', encoding='utf8')
                    print(r.text, file=paper_file)
                    paper_file.close()
                    # print("Paper downloaded.")

        except requests.exceptions.Timeout as e:
            print(e)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        except ET.ParseError as e:
            print(e)
        return

    def download(self, file_dir, save_dir, skip=0):
        """
        Download articles from file
        :param file_dir: Path to file containing file urls
        :param save_dir: Where to save articles
        :param skip: Number of lines to skip
        :return:
        """
        completed_urls = []
        with open(file_dir) as f:
            for line in f.readlines()[skip:]:
                if line.startswith('https://api.elsevier.com/'):
                    url = line.rstrip()
                    self.save_xml(url, save_dir)
                    completed_urls.append(url)

        return completed_urls

    def perform_search(self, query, start=0, show=100):
        """
        Query the Elsevier API
        :param query: Query string
        :param start: paper to start at
        :param show: how many papers to show, determined by elsevier
        :return:
        """
        body = {'display': {'offset': start, 'show': show}}
        body.update(query)
        print(body)
        headers = {'x-els-apikey': self.key,
                   'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        try:
            response = requests.put('https://api.elsevier.com/content/search/sciencedirect',
                                    json=body,
                                    headers=headers)
        except requests.exceptions.Timeout as e:
            print("Timeout exception")
            print(e)
            return None
        # FATAL ERROR
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        return response

    def get_article_urls(self, volume_url, max_articles):
        """ find all article urls from within a Elsevier journal volume index """
        # This page now shows all the articles in the chosen Volume/Issue
        response = requests.get(volume_url)
        if 'Unable to access requested resource' in response.text:
            raise Exception('Unable to find journal at ' + volume_url)
        else:
            article_list = BeautifulSoup(response.text, "lxml").findAll('a')
            if article_list:
                for artcle in article_list[2:]:
                    self.urls.append(artcle['href'])
                    if len(self.urls) >= max_articles:
                        return
            else:
                print("No article urls found in " + volume_url)
        return

    def query(self, query, save_file=None, max_papers=None, skip_papers=0, dir_for_files=None):
        """
        Perform query search on Elsevier API, save all article urls to file
        :param query: Query string
        :param save_file: Name of file to save article urls, if present
        :param max_papers: Number of papers to scrape, Default None
        :param skip_papers: Skip papers, default 0
        :param dir_for_files: Directory where to download the files, if given
        :return:
        """
        # Perform the search query
        response = self.perform_search(query)
        print("SCRAPING ELSEVIER WEBPAGES\n")

        if response is None:
            return

        results = response.json()
        number_of_papers = int(results['resultsFound'])
        number_of_pages = int(number_of_papers/self.elsevier_max_show_value) + 1
        if max_papers is None:
            papers_to_scrape = number_of_papers
        else:
            papers_to_scrape = min(max_papers, number_of_papers)

        print("Total number of papers found: ", number_of_papers)
        print("Number of papers to read: ", papers_to_scrape)
        print("Papers to read: {} - {}".format(skip_papers+1, skip_papers+papers_to_scrape))
        pages_to_read = int(papers_to_scrape/self.elsevier_max_show_value) + 1

        # save urls to file if filename is present
        if save_file:
            for i, start in enumerate(range(skip_papers, skip_papers+papers_to_scrape, self.elsevier_max_show_value)):
                succeeded = False
                print("Reading page " + str(i+1) + "/" + str(pages_to_read))
                if max_papers and \
                        max_papers != self.elsevier_max_show_value and \
                        (i+1)*self.elsevier_max_show_value > max_papers:
                    show = max_papers % self.elsevier_max_show_value
                else:
                    show = self.elsevier_max_show_value
                while not succeeded:
                    try:
                        response = self.perform_search(query, start, show=show)
                        if response is None:
                            return
                        else:
                            results = response.json()
                            if not results['results']:
                                continue
                            else:
                                for r in results['results']:
                                    doi = r['doi']
                                    with open(save_file, 'a+') as wf:
                                        wf.write(doi + '\n')
                                        wf.flush()
                                    if dir_for_files:
                                        self.save_xml_from_doi(doi, dir_for_files)
                                    succeeded = True
                            #time.sleep(0.1)
                    except Exception as e:
                        print("Not succeeded error")
                        print(response, type(response))
                        print(response.json())
                        print(e)
                        continue

        return


