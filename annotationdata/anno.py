#!/usr/bin/env python
#coding:utf-8

import requests
from bs4 import BeautifulSoup   # install BeautifulSoup: pip install beautifulsoup4

class ScratchData():

    def __init__(self, version, url, logs):
        self.version = version
        self.url = url
        self.logs = logs

    def scratchTable(self):
        """
        scratch table from web, and restore the name, title, link
        """
        r = requests.get(self.url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc)
        anno_title = str(soup.title.string)
        table_content = soup.find_all("div", class_="do_not_rebase")
        tr_content = table_content[0].find_all("tr")

        #f = open(self.logs,"w")

        for line in tr_content:
            web_link = [link.get('href') for link in line.find_all('a')]
            td_lst = line.find_all("td")
            package_lst = [str(block.string) for block in td_lst]
            
            #f.write(web_link+'\t'+db_package+"\t"+db_title)
        #f.close()

    
    def writeLogs(self):
        """
        write logs
        """
        pass
    
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
