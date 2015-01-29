#!/usr/bin/env python
#coding:utf-8

import requests
from bs4 import BeautifulSoup   # install BeautifulSoup: pip install beautifulsoup4

import json
#import csv

class ScratchData():

    def __init__(self, version, url):
        self.version = version
        self.url = url

    def scratchTable(self):
        """
        scratch table from web, and restore the name, title, link
        """
        r = requests.get(self.url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc)
        table_content = soup.find("div", class_="do_not_rebase").find("table").find_all("tr")
        log_lst = []
        for line in table_content:
            log_dict = {}
            table_text = [unicode(block.string) for block in line.children]
            log_dict['package'] = table_text[1]
            log_dict['title'] = table_text[5]
            for link in line.find_all('a'):
                log_dict['package_link'] = unicode(link.get('href'))
            log_lst.append(log_dict)
        return log_lst[1:]

    def writeLogs(self, logfile):
        """
        write logs
        """
        content = self.scratchTable()
        with open(logfile, "wb") as lf:
            lf.write(json.dumps(content))

    def downLoadFiles(self, restore_dir):
        """
        download the file by the link in the logs
        """
        pass


    def unzipFile(self):
        """
        tar -xzvf the file
        """
        pass

    def readData(self, filesqlite):
        """
        read data from file of sqlite and restor to another csv
        """
        pass
