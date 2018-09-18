import urllib.request
from bs4 import BeautifulSoup
import sys
import requests

url = "https://www.budgetbytes.com/category/recipes/"

page_append = "/page/"

urls = []

def getSite(url):
    site = urllib.request.urlopen(url)
    return BeautifulSoup(site, 'html.parser')

for page in range(1,21):
    soup = getSite(url + page_append + str(page))
    links = soup.findAll("a", rel="bookmark")
    for link in links:
        print(link.get("href"))
