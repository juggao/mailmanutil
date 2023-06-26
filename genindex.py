#!/usr/bin/env python3
#
#  Generates a html index file from a Mailman archive directory sorted by subject
#
#  Edit the paths below to the mailman archive to suit your needs
#
#  You can fetch mailman archives with this repo:
#       https://github.com/philgyford/mailman-archive-scraper/
#
#
from bs4 import BeautifulSoup
import errno
import os
import sys

web_url= "http://www.tuxtown.net/pipermail/d66/"
index="/run/media/reinold/SEAGATE/sites/tuxtown/index.html"
htmlindexfile="/run/media/reinold/SEAGATE/sites/tuxtown/d66index.html"
walk_dir="/run/media/reinold/SEAGATE/sites/tuxtown/html"

print('walk_dir = ' + walk_dir)

htmlstr="""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
  <HEAD>
     <title>The D66 Archive by thread</title>
     <META NAME="robots" CONTENT="noindex,follow">
     <META http-equiv="Content-Type" content="text/html; charset=utf-8">
 </head>
  <BODY BGCOLOR="#ffffff">
"""

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

def fetchfile(htmlfile):
	page = open(htmlfile)
	source = page.read()
	page.close()
	return source

if __name__ == "__main__":
    links=set()	
    subjects=[]
    for root, subdirs, files in os.walk(walk_dir):
        list_file_path = os.path.join(root, 'date.html')
        pos = list_file_path.find('html/')
        pos2 = list_file_path.rfind('/')
        date = list_file_path[pos+5:pos2]

        source1 = fetchfile(list_file_path)
        if (source1 != None):
            soup1 = BeautifulSoup(source1, 'html.parser')
        for link in soup1.findAll('a'):
            if (link.string != None):
                if ((link.string.find('[ thread ]') >= 0) or
                    (link.string.find('[ subject ]') >= 0) or
                    (link.string.find('More info on this list...') >= 0) or 
                    (link.string.find('[ author ]') >= 0)):
                    pass
                else:
                    href=link.get('href')
                    url= ""
                    if (href != None):
                        url = web_url + date + '/' + href
                        link['href'] = link['href'].replace(href, url)
                        print(url)
                        try: 
                            p = subjects.index(link.string)
                        except ValueError:
                            links.add(link)
                            #print(link.string)
                            subjects.append(link.string)

	# sort
    newlinks = sorted(links, key=lambda links: links.string)
    lnks = list(newlinks)

    Html_file= open(htmlindexfile,"w")
    Html_file.write(htmlstr)
    for l in lnks:
        if (l.string != None):
            print(l.string)
            Html_file.write('\n<LI><A HREF=\"')
            Html_file.write(l.get('href'))
            Html_file.write('\">')
            Html_file.write(l.string.strip())
            Html_file.write('</A>\n')			
    Html_file.write('</BODY></HTML>')
    Html_file.close()



