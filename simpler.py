import subprocess


def linkedIn_Scapper(url):
	file = open(url, 'rb')
	data = file.read()
	data = data[1:-1]
	
	start = data.find('<')
	while start != -1:
		start = data.find(' ', start)
		end = data.find('>')
		front = data[:start]
		back = data[end+1:]
		data = front+back
	print(data)
linkedIn_Scapper("profile.html")