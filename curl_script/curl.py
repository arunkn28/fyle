import requests

print("First API with limit 3 and offset as 0")
url = "http://fyle-apis.herokuapp.com/api/branches/autocomplete?q=RTGS&limit=3&offset=0"

response = requests.get(url)
print(response.text)

print("Second API with limit 2 and offset as 1")
url = "http://fyle-apis.herokuapp.com/api/branches?q=Bangalore&limit=2&offset=1"

response = requests.get(url)
print(response.text)
