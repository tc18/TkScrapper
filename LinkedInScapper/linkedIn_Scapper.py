import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import svgwrite
import xlsxwriter

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
    
    a = []
    for i in schools:
        schoolNameTag = (i.find("h4", { "class" : "item-title" }))
        schoolNameATag = (i.find("a", { "data-tracking-control-name" : "pp_sprof"}))
        schoolName = bettag(schoolNameATag)
        DegreeName = (i.find("h5", { "class" : "item-subtitle" }))
        DegreeTag = (i.find("span", { "class" : "translated translation"}))
        Degree = bettag(DegreeTag).split(',')
        time = (i.find("span", { "class" : "date-range" }))
        timespan = tagsBettag(time)  ###------------------------------------
        #print(b'\xe2\x80\x93'.decode('utf-8'))
        a.append([schoolName, Degree[0], Degree[1]])
        
    profile['education'] = a
        
    #4) Experience
    profile['experience'] = OrderedDict()
    details = (soup.find_all("section", { "id" : "experience" }))
    positions_data =  BeautifulSoup(str(details)[1:-1], "html.parser")
    positions = (positions_data.find_all("li", { "class" : "position" }))
	
    a = []
    for i in positions:
        positionsTag = (i.find("h4", { "class" : "item-title" }))
        positionsTag = bettag(tagsBettag(positionsTag))
        companyTag = (i.find("h5", { "class" : "item-subtitle" }))
        companyTag =  bettag(tagsBettag(companyTag))
        time = (i.find("span", { "class" : "date-range" }))
        time = timeTag(tagsBettag(time))
        a.append([companyTag,positionsTag,time])
		#print(positions)
   
    profile['experience'] = a
    
	#5)Skills  
    profile['skills'] = OrderedDict()
    details = (soup.find_all("section", { "class" : "profile-section skills-section" }))
    skills_data =  BeautifulSoup(str(details)[1:-1], "html.parser")
    skills = (skills_data.find_all("span", { "class" : "wrap" }))
    
    a = []	
    for i in skills:
        skill = bettag(tagsBettag(i))
        a.append(skill)
    profile['skills'] = a
    
    #######################################################################################
    #print(profile)
    r = json.dumps(profile)
    with open('data.json', 'w') as f:
        f.write(r)
		
    workbook = xlsxwriter.Workbook('hello.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Item')
    worksheet.write('B1', 'Cost')
    row = 1
    col = 0
    sorted(profile)
    for i in (profile):
        print(i)
        worksheet.write(row, col,     profile[i])
        worksheet.write(row, col + 1, profile[i])
        row += 1
    workbook.close()
    #createSVG(r)
    #print(r)
	
def timeTag(string):
    a = []
    data = string[6:]
    a.append(data[:data.find('<')])
    data = data[37:]
    a.append(data[:data.find('<')])
    data = data[data.find('<')+9:-1]
    a.append(data[:data.find('<')])
    return a
	
def tagsBettag(string):
    data = str(string)
    start = data.find('<')
    end = data.find('>')
    end1 = data[::-1].find('<')
    return data[end+1:len(data)-end1]
    
def bettag(string):
    data = str(string)
    start = data.find('<')
    end = data.find('>')
    start1 = data.find('<',end)
    return data[end+1:start1]

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
    dwg.add(dwg.g)
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