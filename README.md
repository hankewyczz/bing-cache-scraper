# Bing Cache Scraper

---

This is a quick Python script for crawling Bing and recovering any saved cached pages. This is mainly helpful for situations where a site has suddenly dissapeared (or if your site host lost your data). 

## Why Bing?

Bing has few restrictions on bots, and also (in my experience) keeps page caches for longer than Google. 

## Usage

Open bing-cache-downloader.py, and enter the website, the number of pages you want to retrieve, and any additional arguments. Additional arguments are useful in cases where there are pages you don't want to recover.

The script should automatically save and format all of the files in /save/, but in case this doesn't work (no reason it shouldn't), the URLs can be manually downloaded using wget, like so: wget -k -E -p -i cached_urls.txt

