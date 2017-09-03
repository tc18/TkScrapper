import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import svgwrite

'''
!important things
everylink has some specials attribute
to get data, those attribute must be same.
'''

def linkedIn_Scapper(url):
	file = open(url, 'rb')
	data = file.read()
	profile = OrderedDict()
	
	#parse html data in BeautifulSoup 
	soup = BeautifulSoup(data, "html.parser")
	
	#1) Photo_Link must be in <a> tag and class should be 'photo'
	photo = soup.find_all("a", { "class" : "photo" })
	profile["photo"] = link_href(photo)
	
	#2) User Details
	profile['userDetails'] = OrderedDict()
	details = remove(soup.find_all("h1", { "id" : "name" }))
	profile['userDetails']["userName"] = details
	headline = remove(soup.find_all("p", { "class" : "headline title" }))
	profile['userDetails']["headline"] = headline
	location = remove(soup.find_all("span", {"class" : "locality"}))
	profile['userDetails']["location"] = location
	industry = remove(soup.find_all("dd", {"class" : "descriptor"}))
	profile['userDetails']["industry"] = industry
	connections = remove(soup.find_all("div", {"class" : "member-connections"}))
	profile['userDetails']["connections"] = connections
	
	#3) Education
	profile['education'] = OrderedDict()
	details = (soup.find_all("ul", { "class" : "schools" }))
	school_data =  BeautifulSoup(str(details)[1:-1], "html.parser")
	schools = (school_data.find_all("li", { "class" : "school" }))
	
	#print(schools)
	
	##############################
	r = json.dumps(profile)
	with open('data.json', 'w') as f:
		f.write(r)
	createSVG(r)
	print(r)
	
def remove(string):
	#print(string)
	data = str(string)
	data = data[1:-1]
	start = data.find('<')
	while start>=0:
		end = data.find('>')
		front = data[:start]
		back = data[end+1:]
		data = front+back
		start = data.find('<')
	return data

def createSVG(data):
	with open('data.html', 'w') as f:
		f.write('<html><head><title>GraphPython</title><script> function readSVG(){ alert("Chintan"); var rawFile = new XMLHttpRequest();    rawFile.open("GET", "test.svg", true);    rawFile.onreadystatechange = function ()    {        if(rawFile.readyState === 4)        {            var allText = rawFile.responseText;            document.getElementById("textSection").innerHTML = allText;        }}    rawFile.send(); }readSVG();</script></head><body><div id="textSection" style="width"></div></body></html>')
	dwg = svgwrite.Drawing('test.svg', profile='tiny')
	dwg.add(dwg.g
	dwg.add(dwg.circle(center=(0, 0), r=500, stroke=svgwrite.rgb(255,0,0,'%')))
	dwg.add(dwg.text('Test', insert=(0, 2), fill='red'))
	dwg.save()

def link_href(link):
	string = str(link)
	start_sign = 'href="'
	start = string.find('href="')
	end = string.find('"',start+len(start_sign))
	return string[start+len(start_sign):end]
	
	
linkedIn_Scapper("profile.html")