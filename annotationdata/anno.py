#!/usr/bin/env python
#coding:utf-8

import requests
from bs4 import BeautifulSoup   # install BeautifulSoup: pip install beautifulsoup4
import tarfile
import wget

class ScratchData(object):
    """
    get Bioconductor AnnotationData Packages from the website of Bioconductor
    for example, Bioconductor 3.0, the url is http://www.bioconductor.org/packages/3.0/data/annotation/
    """

    def __init__(self, download_url, db_directory):
        self.url = download_url
        self.db_dir = db_directory

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

        return todo_lst

    def packageFilesUrl(self):
        """
        get the URL of packages with '.gz' as their extension.
        """
        source_link = self.usefulTable()
        db_link = [element['package_link'] for element in source_link ]
        link = [self.url + '/' + str(short_link) for short_link in db_link]
        file_link = []

        for dl_link in link:
            dr = requests.get(dl_link)
            dl_html = dr.text
            soup = BeautifulSoup(dl_html)
            gz_link = soup.find("div", class_="do_not_rebase").find_all("table")[2].find_all('td')[1].a.get('href')
            all_link = self.url + "".join(list(gz_link)[2:])
            file_link.append(all_link)
        return file_link

    def downloadPackage(self):
        """
        download the packages(.gz) from their URL
        """
        packages_link = self.packageFilesUrl()

        out_dir = self.db_dir
        if out_dir[-1] != '/':
            out_dir += "/"

        file_name_lst = []
        #for p_url in packages_link[1:3]:   #you can limit some of the packages.
        for p_url in packages_link:
            print "downloading:\n"
            file_name = wget.download(str(p_url), out=out_dir)
            file_name_lst.append(file_name)
        print "\nended download."

        return file_name_lst


    def unzipFile(self):
        """
        extract the packages with '.gz' as their extension
        """
        gz_files = self.downloadPackage()

        db_dir = self.db_dir

        if db_dir[-1] != '/':
            db_dir += '/'

        print "unzip the file(*.gz)"

        for filename in gz_files:
            #path_filename = db_dir + filename
            path_filename = filename
            tar = tarfile.open(path_filename)
            tar.extractall(path=db_dir)
            tar.close()

        return gz_files
