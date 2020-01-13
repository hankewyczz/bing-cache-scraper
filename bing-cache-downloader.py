import urllib.request
import urllib.parse
from urllib.parse import unquote
import time
import datetime
import io
import os
from bs4 import BeautifulSoup

def cache_scraper(query, total):
	# Just some headers so Bing stops screaming at us
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	values = {'name' : 'Notta Robot',
	          'location' : 'Chicago',
	          'language' : 'Python' }
	headers = { 'User-Agent' : user_agent }
	data = urllib.parse.urlencode(values)
	data = data.encode('ascii')

	cached_urls = []
	for i in range(1, total, 14):  # Decides which page to start at, 14 per page
		search_page = 'http://www.bing.com/search?q=%s&first=%d' % (query, i)
		req = urllib.request.Request(search_page, data, headers)
		with urllib.request.urlopen(req) as response:
		   raw_page = response.read()
		text = raw_page.decode('utf-8')
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
		time.sleep(1) # Not necessary, but lets you read which URLs are being copied

	return cached_urls


def download_cached(cached_pages):
	# Just some random headers so Bing stops screaming at us
	headers = {
	    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
	    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
	    'Content-Type': 'application/x-www-form-urlencoded'
	}
	for page in cached_pages:  # Iterates thru all the links
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

		date = soup.find_all("div")[3]
		date = date.strong.text
		#mainContent = "<center><h2>Cached on " + date + "</h2></center><br><br>" + mainContent
		# ^ This just adds the cached date, if you need it for comparison (ie. compare against google's cache)
		title = unquote(soup.base['href']).split("/")[-1]
		title = title.replace(":","-")
		title = title.replace("?", "")
		fpath = "save/%s.html" % title
		with io.open(fpath, "w+", encoding="utf-8") as f:
			f.write(mainContent)
		timestamp = time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y").timetuple())
		os.utime(fpath, (timestamp, timestamp))


def main():
	website = "wikispiv.com" 
	args = " -user" 			# any filter arguments?
	query_raw = "site:" + website + args
	query = urllib.parse.quote(query_raw)
	print(query)
	number_of_pages = 600
	
	cached_pages = cache_scraper(query, number_of_pages)
	cached_pages = list(set(cached_pages)) # Remove duplicates	

	## Manual Backup ##
	# write cache urls only to text file for easy scrape with wget
	with open("cached_urls.txt", "a+") as f:
		for line in cached_pages:
			f.write("%s\n" % line)
	# Use wget to grab the pages (-k -E -p -i cached_urls.txt)

	# Grab the cached URLs of the results
	download_cached(cached_pages)

if __name__ == "__main__":
    main()