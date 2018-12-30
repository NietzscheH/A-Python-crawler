from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import re

# Get links of all downloadable books from thoreausociety.org
dic = {} # A dictionary with books' names as keys
html = urlopen("http://www.thoreausociety.org/basic-page/writings").read()
soup = BeautifulSoup(html, features='lxml')
links = soup.find_all('a', {'class': 'caption'})

for i in links:
    dic[i.get_text()] = i['href']

# dic[''] is actually thoreausociety.org; ignore it
del dic['']
# most books are from archive.org but there are three books that are from Google.book; I just delete them for the purpose of convenience
del dic['A Walk to Wachusett']
del dic['The Landlord']
del dic['Thomas Carlyle and his Works']

# Another dictionary with books' names as keys
download_dic = {}
for key in dic:
    html_ = urlopen(dic[key]).read()
    soup_ = BeautifulSoup(html_, features='lxml')
    download_links = soup_.find_all('a', {'href': re.compile('.*?\.pdf')}) # find the url ending with .pdf
    download_dic[key] = 'https://archive.org' + download_links[0]['href'] # modify the url to make it feasible
    urlretrieve(download_dic[key], 'Desktop/%s.pdf' % key) # download pdf
