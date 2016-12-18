#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests,re,json,urllib,os

def fix(string):
	string = string[:string.index("\\")]+"\n"+string[string.index("\\")+2:]
	return string



APP_KEY = "4fac7cf09e339c2c2eb1"
APP_SECRET = "55a8673c229435c1010c9726f558eea57a80351d"
CALLBACK_URL = 'https://api.shanbay.com/oauth2/auth/success/'
authorize_url = "https://api.shanbay.com/oauth2/authorize/?client_id=%s&response_type=code&state=123" %APP_KEY

#program start
s = requests.Session()
print "Please enter the website and get the code:",authorize_url
code = raw_input("Please enter the code:")
token_url = "https://api.shanbay.com/oauth2/token/"
values = {
	"client_id": "4fac7cf09e339c2c2eb1",
	"client_secret": "55a8673c229435c1010c9726f558eea57a80351d",
	"grant_type": "authorization_code",
	"code": "%s" %code,
	"redirect_uri": "https://api.shanbay.com/oauth2/auth/success/",
}

r = s.post(token_url,values)
access_token = re.findall(r'"access_token": "(.*?)",',r.text)[0]

while True:
	word = raw_input("Please enter the word you wanna search:")
	search_url = "https://api.shanbay.com/bdc/search/?word=%s" %word 
	r = s.get(search_url).text
	file = json.loads(r)
	if  file["status_code"] == 0:
		ID = file["data"]['id']
		temp = {}
		temp["cn_definition"] = file["data"]["definition"]
		en_definition = file["data"]["en_definition"]["pos"] + '. ' + file["data"]["en_definition"]["defn"]
		cn_definition = re.findall(r'{"cn_definition": " (.*?)"}',json.dumps(temp,ensure_ascii=False))[0]
#		audio = file["data"]["audio"] #audio path
#		urllib.urlretrieve(audio, "audio.mp3")  #download the audio
		while	"\\" in cn_definition:
			cn_definition = fix(cn_definition)
		
		print "\n "+word+'\n'
		print en_definition
		print cn_definition + '\n'

#		os.system("mpg321 audio.mp3 -q")
		data = {}
		data['id'] = ID
		add_url = "https://api.shanbay.com/bdc/learning/?state=123&access_token=%s" %access_token	
		r = s.post(add_url,data)
		os.remove("audio.mp3")
	else:
		print "Not a legal word"
			
	