# Bing Cache Scraper

---

## Functionality

This script crawls Bing and recovers any saved cached pages. This is mainly helpful for situations where a site has suddenly disappeared (or in my case, if your site host lost your data). The script includes some formatting features to strip Bing's additions to cached pages. 

## Why Bing?

Bing has few restrictions on bots, and also (in my experience) keeps page caches for longer than Google. 

## Usage

Open bing-cache-downloader.py, and enter the website, the number of pages you want to retrieve, and any additional arguments. Additional arguments are useful in cases where there are pages you don't want to recover (eg. exclude any profile pages by adding "-profile" as an argument). 

The script automatically saves and formats all of the files in `/save/` . Alternativly, the URLs can be manually downloaded using `wget`, like so: `wget -k -E -p -i cached_urls.txt`

