from urllib import request, parse
import datetime
import io
import os
from bs4 import BeautifulSoup

# Just some headers so Bing stops screaming at us
headers = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

def cache_scraper(query, total):
	cached_urls = []
	for i in range(1, total, 14):  # Decides which result to start at, 14 per page
		search_page = 'http://www.bing.com/search?q=%s&first=%d' % (query, i)
		raw_page = request.urlopen(search_page).read()
		text = raw_page.decode('utf-8')
		# Parses the HTML
		soup = BeautifulSoup(text, 'html.parser')
		cached_list = soup.find_all("div", class_="b_attribution")	# Grabs the main divs from all the results

		for link in cached_list:
			orig_url = link.cite.get_text()		# Grabs the original URL, just to visually see what results are being gotten
			cache_str = link.get('u')
			if (cache_str != None):
				cache_str_split = cache_str.split('|')
				cache_url = "http://cc.bingj.com/cache.aspx?q=%s&d=%s&mkt=en-US&setlang=en-US&w=%s" % (query, cache_str_split[2], cache_str_split[3])
			print(orig_url)
			cached_urls.append(cache_url)
	return cached_urls

def download_cached(cached_pages):
	for page in cached_pages:  # Iterates thru all the links
		raw_page = request.urlopen(page).read()
		text = raw_page.decode('utf-8')
		soup = BeautifulSoup(text, 'html.parser')

		## Remove the things bing adds, restores original format
		mainContent = soup.find_all("div", class_="cacheContent")
		mainContent = mainContent[0]
		for div in mainContent.find_all("div", class_="printfooter"):
			div.decompose()
		# Grabs the title from the page (to use as the filename)
		title = mainContent.title.string
		mainContent = str(mainContent)
		# Grabs the date cached, so that it can be compared to other caches (eg. google)
		date = soup.find_all("div")[3]
		date = date.strong.text
		#mainContent = "<center><h2>Cached on " + date + "</h2></center><br><br>" + mainContent
		# ^ This just adds the cached date, if you need it for comparison (ie. compare against google's cache)
		
		# Grabs the original title of the page
		title = parse.unquote(soup.base['href']).split("/")[-1]
		# Formats the string to be a valid filename
		replaceChars = (' ',':','?')
		oldTitle = str(title)
		title = ""
		for c in oldTitle:
			if c.isalnum or c == "," or c == "-" or c == "_":
				title += c
			elif c in replaceChars:
				title += "_"
		# Subdirectory to save the files in
		dirName = 'save' 
		if not os.path.exists(dirName):
			os.mkdir(dirName)
		fpath = "%s/%s.html" % (dirName, title)
		with io.open(fpath, "w+", encoding="utf-8") as f:
			f.write(mainContent)
		# Changes the date modified of the file to match the date cached (useful for comparing different cached versions)
		timestamp = datetime.datetime.strptime(date, "%m/%d/%Y").timestamp()
		os.utime(fpath, (timestamp, timestamp))

def main():
	website = "wikispiv.com" 
	args = " -user" 			# any filter arguments?
	query_raw = "site:" + website + args
	query = parse.quote(query_raw)
	number_of_pages = 600
	
	cached_pages = cache_scraper(query, number_of_pages)
	cached_pages = list(set(cached_pages)) # Remove duplicates	

	#w Manual Backup - writes the cache urls to a txt file for wget scraping
	with open("cached_urls.txt", "a+") as f:
		for line in cached_pages:
			f.write("%s\n" % line)
	# If using wget : (-k -E -p -i cached_urls.txt)

	# Download the cached pages
	download_cached(cached_pages)

if __name__ == "__main__":
    main()