from bs4 import BeautifulSoup
import bs4
import sqlite3
soup=BeautifulSoup(open("cobuild.xml"),"xml")
db=sqlite3.connect("./english.db")
db.text_factory=str
cnt=0
for item in soup.find_all('entry'):
	cnt=cnt+1
#print "========="
	key=item.attrs["id"].encode("utf-8")
	print cnt,key
#	print "--------------------"
	value=item.encode("utf-8")
#print value
	db.execute("insert into xml values(?,?)",(key,value))
	if(cnt%1000==0):
		db.commit();
db.commit()
#print item.encode(formatter="html")
#print item.namespace
#	a=item.attrs["id"]
#	print a.encode("utf-8")
#tmp=soup.new_tag(a)
#	print type(tmp)
#print tmp.prettify(formatter="html")
#print item.name
#print str(item)
#print "=========="
#	raw_input()
