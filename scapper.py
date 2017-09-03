import urllib.request
from bs4 import BeautifulSoup

def scapLinkedIn(url):
	urlopener= urllib.request.build_opener()
	urlopener.addheaders = [('User-agent', 'Mozilla/5.0')]
	page= urlopener.open(url).read()
	#print(page)
	
	data = str(page)
	soup = BeautifulSoup(data)
	profile = soup.find_all("div", { "id" : "profile" })
	print(profile)
	
	'''response = urllib.request.urlopen(url)
	page = response.read()'''
	
	html = str(page)
	start = html.find('<div id="profile">')
	#print (start)
	end = html.find('<div id="aux">')
	user_data = html[start:end]
	#print(user_data)
	fo = open(url+".html", "wb")
	fo.write(page);
	fo = open(url+".html", "wb")
	fo.write((str(profile)).encode('utf8'));

scapLinkedIn("https://www.linkedin.com/in/kishankathiriya/")
#scapLinkedIn("https://www.google.com")