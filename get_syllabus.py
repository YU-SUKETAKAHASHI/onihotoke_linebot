import requests
from bs4 import BeautifulSoup






# r_get = requests.get("https://craft.cite.tohoku.ac.jp/qsl/syllabus/search?type=zengaku")#, data=keyword)
# soup = BeautifulSoup(r_get.text, 'lxml')
# _csrf = soup.input.get("value")
# print(r_get.headers)
# print(_csrf)
keyword = {"query_string":"人間論"}
# headers = {"X-CSRF-Token":_csrf}

URL = "https://craft.cite.tohoku.ac.jp/qsl/syllabus/search?type=zengaku"

session = requests.session()
res = session.get(URL)
print(session.headers)
csrf = session.cookies['csrf']
print(csrf)
r_post = requests.post(URL, headers=headers, data=keyword)

# print(r_post.text)
print(r_post.headers)