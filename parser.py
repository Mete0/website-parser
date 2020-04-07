from bs4 import BeautifulSoup
import urllib3, re, requests, json, os

os.chdir("/home/meteo/gw2alerts/")

with open('mailed.json') as f:
    mailed = json.load(f)

http = urllib3.PoolManager()
url = 'https://en-forum.guildwars2.com/discussion/458/news-gemstore-items-new-returned-sales'
response = http.request('GET', url)
soup = BeautifulSoup(response.data, "html.parser")
lastpage = soup.find(attrs={'class': 'LastPage'})
lastpage_url = lastpage.attrs['href']
response = http.request('GET', lastpage_url)
soup = BeautifulSoup(response.data, "html.parser")
message_list = soup.find_all(attrs={'class': 'ItemComment'})
last_message = message_list[-1]

pattern = "Season 3"
if re.search(pattern, last_message.text, re.IGNORECASE) and not mailed.season3:
    requests.post('http://skynet-alpha.appspot.com/send_mail',
                  data={'message': pattern + " is on sale"})
    mailed.season3 = 1

pattern = "copper"
if re.search(pattern, last_message.text, re.IGNORECASE) and not mailed.copper:
    requests.post('http://skynet-alpha.appspot.com/send_mail',
                  data={'message': pattern + " is on sale"})
    mailed.copper = 1

with open('mailed.json', 'w') as outfile:
    json.dump(mailed, outfile)
