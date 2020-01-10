import urllib.request
import urllib.parse
import time
import io
from bs4 import BeautifulSoup

# Just some headers so Bing stops screaming at us
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

page = "http://cc.bingj.com/cache.aspx?q=site%3Awikispiv.com%20-user&d=4763294924473303&mkt=en-US&setlang=en-US&w=_7_8_M4P3uh2GMjiH5CJDNcmH2IuBLXH"
req = urllib.request.urlopen(page)
raw_page = req.read()
text = raw_page.decode('utf-8')
soup = BeautifulSoup(text, 'html.parser')

## Remove the things bing adds, restores original format
mainContent = soup.find_all("div", class_="cacheContent")
mainContent = mainContent[0]
for div in mainContent.find_all("div", class_="printfooter"):
	div.decompose()
title = mainContent.title.string
mainContent = str(mainContent)

with io.open("%s.html" % title, "w+", encoding="utf-8") as f:
	f.write(mainContent)