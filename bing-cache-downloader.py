from urllib import request, parse
import datetime
import io
import os
from bs4 import BeautifulSoup


website = "wikispiv.com" 
args = " -user" 			# any filter arguments?
# Just some headers so Bing stops screaming at us
headers = {
	'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
	'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
	'Content-Type': 'application/x-www-form-urlencoded'
}


# Opens a URL and parses the bfSoup
def parseSoup(page):
	rawPage = request.urlopen(page).read()
	text = rawPage.decode('utf-8')
	# Parses the HTML
	return BeautifulSoup(text, 'html.parser')


## Scrapes all the divs from the search results
def scrapeSearchResults(query, total):
	cachedURLs = []
	for i in range(1, total, 14):  # Decides which result to start at, 14 per page
		searchPage = 'http://www.bing.com/search?q=%s&first=%d' % (query, i)
		soup = parseSoup(searchPage)

		# Grabs the main divs from all the results
		cachedResults = soup.find_all("div", class_="b_attribution")

		cachedURLs.append(paserSearchResults(cachedResults, query))


	return cachedResults


## Parses the search results to get the URLS
def parseSearchResults(cachedResults, query):
	cacheURLs = []
	for link in cachedResults:
		# originalURL = link.cite.get_text()   # Grabs the original URL, to visually see what results are being gotten
		cacheStr = link.get('u')
		if (cacheStr != None):
			cacheStrSplit = cacheStr.split('|')
			cacheURL = "http://cc.bingj.com/cache.aspx?q={0}&d={1}&mkt=en-US&setlang=en-US&w={2}"
			.format(query, cacheStrSplit[2], cacheStrSplit[3])
		cacheURLs.append(cacheURL)
	return cacheURLs




# Generates a valid filename and save path
def saveCached(title):
	# Formats the string to be a valid filename
	newTitle = ""
	for c in title:
		if c.isalnum or c == "," or c == "-" or c == "_":
			newTitle += c
		elif:
			newTitle += "_"

	# Subdirectory to save the files in
	dirName = 'save' 
	if not os.path.exists(dirName):
		os.mkdir(dirName)
	return "%s/%s.html" % (dirName, newTitle)



## Downloads the list of cached pages
def downloadCached(cachedPages):
	for page in cachedPages:  # Iterates thru all the links
		soup = parseSoup(page)

		## Remove the things bing adds, restores original format
		mainContent = soup.find_all("div", class_="cacheContent")[0]

		for div in mainContent.find_all("div", class_="printfooter"):
			div.decompose()

		# Grabs the date cached, so that it can be compared to other caches (eg. google)
		date = soup.find_all("div")[3]
		date = date.strong.text
		
		# Grabs the original title of the page
		title = parse.unquote(soup.base['href']).split("/")[-1]
		fpath = saveCached(title)

		with io.open(fpath, "w+", encoding="utf-8") as f:
			f.write(str(mainContent))
		# Changes the date modified of the file to match the date cached (useful for comparing different cached versions)
		timestamp = datetime.datetime.strptime(date, "%m/%d/%Y").timestamp()
		os.utime(fpath, (timestamp, timestamp))


def main():
	rawQuery = "site:" + website + args
	query = parse.quote(rawQuery)
	numberOfPages = 600
	
	cachedResults = scrapeSearchResults(query, numberOfPages)
	cachedResults = list(set(cachedResults)) # Remove duplicates by converting to set, then back to list

	#w Manual Backup - writes the cache urls to a txt file for wget scraping
	with open("cached_urls.txt", "a+") as f:
		for line in cachedResults:
			f.write("%s\n" % line)
	# If using wget : (-k -E -p -i cached_urls.txt)

	# Download the cached pages
	downloadCached(cachedResults)

if __name__ == "__main__":
	main()