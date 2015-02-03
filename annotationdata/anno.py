#!/usr/bin/env python
#coding:utf-8

import requests
from bs4 import BeautifulSoup   # install BeautifulSoup: pip install beautifulsoup4
import tarfile
import wget
import csv
import os
import os.path

from setting import *

class ScratchData(object):
    """
    get Bioconductor AnnotationData Packages from the website of Bioconductor
    for example, Bioconductor 3.0, the url is http://www.bioconductor.org/packages/3.0/data/annotation/
    """

    def __init__(self, download_url, gz_dir=GZPACKAGE_DIR, ex_dir=EXTRACTED_DIR, log=LOG):
        self.url = download_url
        self.gz_dir = gz_dir
        self.ex_dir = ex_dir
        self.log = log

    def scratchTable(self):
        """
        get the column of the Package and the link, the column of the Title
        """
        print "scratching...", self.url

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
        """
        screen the packages withe '.db' as their extension.
        """
        content = self.scratchTable()

        todo_lst = []

        for line in content:
            package_name = line['package']
            if "." in package_name:
                if package_name.split('.')[1] == 'db':
                    todo_lst.append(line)
        
        #write them into a tmplog.csv file.
        with open("tmplog.csv",'wb') as csv_file:
            writer = csv.writer(csv_file, delimiter='\t')
            for line in todo_lst:
                writer.writerow((line['package'], line['title']))

        return todo_lst

    def packageFilesUrl(self):
        """
        get the URL of packages with '.gz' as their extension.
        """
        source_link = self.usefulTable()
        db_link = [element['package_link'] for element in source_link ]
        
        header_url = self.url+'/' if self.url[-1] != '/' else self.url

        link = [header_url + str(short_link) for short_link in db_link]
        file_link = []

        for dl_link in link:
            dr = requests.get(dl_link)
            dl_html = dr.text
            soup = BeautifulSoup(dl_html)
            gz_link = soup.find("div", class_="do_not_rebase").find_all("table")[2].find_all('td')[1].a.get('href')
            all_link = self.url + "".join(list(gz_link)[2:])    # complete URL of every .gz package.
            file_link.append(all_link)
        
        return file_link
    
    
    def checkPackage(self, directory):
        files_lst = os.listdir(directory)
        if files_lst:
            return files_lst
        else:
            return False 

    def downloadPackage(self):
        """
        download the packages(.gz) from their URL
        """
        packages_link = self.packageFilesUrl()
        
        makeDir(self.gz_dir)  # check self.gz_dir
        
        out_dir = self.gz_dir[0:-1] if self.gz_dir[-1] == '/' else self.gz_dir
        
        #check in the self.gz_dir,is there some package? if ok,then will not download them.
        
        have_packages = self.checkPackage(self.gz_dir)
        if have_packages:
            for have_name in have_packages:
                for every_url in packages_link:
                    package_url, will_name = os.path.split(every_url)
                    if will_name == have_name:
                        packages_link.remove(every_url)

        dir_gzfiles = []
        for p_url in packages_link[0:1]:   #you can limit some of the packages.
        #for p_url in packages_link:
            print "\ndownloading:"
            file_name = wget.download(str(p_url), out=out_dir)
            dir_gzfiles.append(file_name)
        
        download_number = len(dir_gzfiles)
        print "\nHave downloaded .gz packages: ", download_number
        print "\n",dir_gzfiles
        print "\nended download. the packages are in ", self.gz_dir


    def extractGzFiles(self):
        """
        extract the packages with '.gz' as their extension
        """
        
        try:
            gz_files = os.listdir(self.gz_dir)
            gz_dir = self.gz_dir+'/' if self.gz_dir[-1] != '/' else self.gz_dir 
            gz_files = [gz_dir+gz_name for gz_name in gz_files]
            
            print "extract the file(*.gz)"
            makeDir(self.ex_dir)
            for filename in gz_files:
                tar = tarfile.open(filename)
                tar.extractall(path=self.ex_dir)
                tar.close()

            print "have extracted the files into directory: ", self.ex_dir

        except:
            print "There is no .gz Packages. Please download it firltly."

