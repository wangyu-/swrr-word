from bs4 import BeautifulSoup
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
soup.a.string="aaa"
print soup.a.string
