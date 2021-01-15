from bs4 import BeautifulSoup
import requests
import os, os.path, csv 
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque

#url = "https://www.youtube.com"
url = "https://scrapethissite.com"

new_urls = deque([url])
processed_urls = set()
local_urls = set()
foreign_urls = set()
broken_urls = set()
while len(new_urls):
    url = new_urls.popleft()
    processed_urls.add(url)
    print(url)
    try: 
        response = requests.get(url)
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        broken_urls.add(url)
        continue
    parts = urlsplit(url)
    print(parts)
    base = "{0.netloc}".format(parts)
    print(base)
    strip_base = base.replace("www.", "") 
    print(strip_base)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    print(base_url)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url
    soup = BeautifulSoup(response.text, "lxml")
    for link in soup.find_all('a'):    # extract link url from the anchor    
        anchor = link.attrs['href'] if 'href' in link.attrs else ''
        if anchor.startswith('/'):        
            local_link = base_url + anchor
            print(local_link)
            local_urls.add(local_link)    
        elif strip_base in anchor:        
            local_urls.add(anchor)    
        elif not anchor.startswith("http"):        
            local_link = path + anchor        
            local_urls.add(local_link)    
        else:        
            foreign_urls.add(anchor)
            print(anchor)
        if not link in new_urls and not link in processed_urls:    
            new_urls.append(link)
#listings = []
#for rows in soup.find_all("tr"):
    #if ("oddrow" in rows["class"]) or ("evenrow" in rows["class"]):
        #name = rows.find("div", class_="name").a.get_text()
        
        #listings.append(name)

#with open("out.csv", 'a', encoding='utf-8') as toWrite:
    #writer = csv.writer(toWrite)
    #writer.writerows(listings)
    
print("fetched")