#coding:utf-8
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import sqlite3
db=sqlite3.connect('./english.db')
cur = db.execute('select word from collins')
cnt=0
err=open("not_ok.txt","w")
for x in cur.fetchall():
	print cnt
	word=x[0]
	aa=db.execute('select value from collins where word =?',(word,))
#print type (aa)
#raw_input()
	cont=[y[0] for y in aa.fetchall()][0]
#print cont
#	raw_input()
	if cont.find('柯林斯高阶'.decode("utf-8"))==-1:
#		print word
#		print cont
		err.write(word.encode("utf-8")+'\n')
#print word
#		raw_input()
	cnt=cnt+1

