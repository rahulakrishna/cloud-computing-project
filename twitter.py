from bs4 import BeautifulSoup
from urllib.request import urlopen
import falcon
import json
from falcon_cors import CORS

cors = CORS(allow_origins_list=['http://localhost:3000'])

class TwitterResource(object):
	def on_get(self,req,resp,username):
		print(req)
		print(username)
		# username=raw_input()
		url='https://twitter.com/'+username
		# page=urllib2.urlopen(url).read()
		page = urlopen(url)
		soup = BeautifulSoup(page,"lxml")
		title=soup.title.string
		tweets=soup.find_all('p',class_='tweet-text')
		response=[]
		for tweet in tweets:
			if tweet.string==None:
				response.append(tweet.get_text())
			else:
				response.append(tweet.string)
		resp.status=falcon.HTTP_200
		# resp.body="Hello"
		print(response)
		resp.body=json.dumps(response)

app=falcon.API(middleware=[cors.middleware])

twitter=TwitterResource()

app.add_route('/twitter/{username}',twitter)