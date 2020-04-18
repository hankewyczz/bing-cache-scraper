import unittest
import bingCacheDownloader as bc




# Tests parseSoup
class TestParseSoup(unittest.TestCase):
	def setUp(self):
		self.soup = bc.parseSoup("http://example.com")

	def testSoup(self):
		# Just a basic sanity check to make sure we get the site, and parse it correctly
		self.assertEqual(self.soup.title.string, "Example Domain")
		self.assertEqual(self.soup.h1.string, "Example Domain")





# tests scrapeSearchResults AND parseSearchResults
class TestScrapeParseSearchResults(unittest.TestCase):
	def setUp(self):
		self.cached = bc.scrapeSearchResults("example.com", 14)

	def containsExample(self, string):
		return "example" in string or "http" in string

	def testScrape(self):
		self.setUp()
		for link in self.cached:
			self.assertEqual(True, self.containsExample(link.find("cite").get_text()))

	def makeURL(self, item, query):
		if item != None:
			split = item.split('|')
			return ("http://cc.bingj.com/cache.aspx?q={0}&d={1}"
				"&mkt=en-US&setlang=en-US&w={2}").format(query, split[2], split[3])


	def testParse(self):
		self.setUp()
		for item in self.cached:
			self.url = bc.parseSearchResults([item], 14)

			if len(self.url) != 0:
				self.assertEqual(self.url[0], self.makeURL(item.get('u'), 14))


# Tests saveCached
class TestSaveCached(unittest.TestCase):
	def setUp(self):
		self.s1 = bc.saveCached("example")
		self.s2 = bc.saveCached("exam,ple")
		self.s3 = bc.saveCached("exam-ple")
		self.s4 = bc.saveCached("exam_ple")
		self.s5 = bc.saveCached("exam?ple")

	def testSaveCached(self):
		self.assertEqual("save/example.html", self.s1)
		self.assertEqual("save/exam,ple.html", self.s2)
		self.assertEqual("save/exam-ple.html", self.s3)
		self.assertEqual("save/exam_ple.html", self.s4)
		self.assertEqual("save/exam_ple.html", self.s5)
		

if __name__ == "__main__":
    unittest.main()