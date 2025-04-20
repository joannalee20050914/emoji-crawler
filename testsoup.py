from bs4 import BeautifulSoup
html = "<p>Hello, world!</p>"
soup = BeautifulSoup(html, "html.parser")
print(soup.p.text)