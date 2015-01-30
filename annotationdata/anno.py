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
    
    def usefulTable(self):
        content = self.scratchTable()
        todo_lst = []
        for line in content:
            package_name = line['package']
            if "." in package_name:
                if package_name.split('.')[1] == 'db':
                    todo_lst.append(line)
        return todo_lst

    def writeLogs(self, logfile):
        """
        write logs
        """
        content = self.usefulTable()
        with open(logfile, "wb") as lf:
            lf.write(json.dumps(content))

    def downloadFiles(self, restore_dir):
        """
        download the file by the link in the logs
        """
        source_link = self.usefulTable()
        db_link = [element['package_link'] for element in source_link ]
        link = ["http://bioconductor.org/packages/3.0/data/annotation/"+str(short_link) for short_link in db_link]
        file_link = []

        for dl_link in link:
            dr = requests.get(dl_link)
            dl_html = dr.text
            soup = BeautifulSoup(dl_html)
            gz_link = soup.find("div", class_="do_not_rebase").find_all("table")[2].find_all('td')[1].a.get('href')
            all_link = "http://bioconductor.org/packages/3.0/data/annotation" + "".join(list(gz_link)[2:])
            file_link.append(all_link)
        


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
