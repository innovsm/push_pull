import requests
from bs4 import BeautifulSoup
url = "https://filebin.net/hello32532"
response = requests.get(url, stream=True)

# get all uploaded document link
data = BeautifulSoup(response.text, 'html.parser')
for i in data.find_all("a"):
    print(i.get("href"),"https://filebin.net/hello32532")
