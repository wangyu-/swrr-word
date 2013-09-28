#### -*- coding: utf-8 -*-
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for,abort, render_template, flash
from bs4 import BeautifulSoup
import bs4
EN_DB = '/Users/wangyu/wyflask/english.db'
def connect_en_db():
	return sqlite3.connect(EN_DB)
en_db=connect_en_db()
word='flush'
cur=en_db.execute('select value from collins where word =?',(word,))
value=[row[0] for row in cur.fetchall()][0]
soup = BeautifulSoup(''.join(value))
#print res1
collins_pack={}
collins_pack["list"]=[]
collins_pack["word"]=word
def soup_copy(a):
	tmp=str(a)
	'''
	print "!!!!!"
	print tmp
	print "@@@@@"'''
	tmp2= BeautifulSoup(''.join(tmp))
	'''print tmp2
	print "#####"
	print dir(tmp2)'''
	return tmp2.findChild()
def print_dict(d):
	import json
	print json.dumps(d, encoding="UTF-8",indent=1, ensure_ascii=False)
for res1 in soup.find("div",attrs={"class":"collins"}).findAll("div",attrs={"class":"part_main"}):
	print"======="
	print str(res1)
#raw_input()
	collins_dict={}
	collins_dict["meanings"]=[]
	switch=res1.find(name="h3",class_="menu_switch")
	if switch!=None:
		collins_dict["class"]=switch.get_text(strip=True)
	res1=res1.find(name="div",class_="collins_content")
	for item in res1.findAll(name='div',):#recursive=False):
		attr=dict(item.attrs)
#print item['class']
#	print item.get('class')
#	raw_input()
		if(attr.has_key("class") and attr["class"][0]=="collins_en_cn"):
			'''print "---------------"
			print item
			print "==============="'''
			item2=item.find(name='div',attrs={'class':'caption'},recursive=False)
			if(item2==None):
				continue
			print type(item2)
			print item2.attrs["class"]
			if(len(item2.attrs["class"])!=1):
				continue
			meaning={}
			print "------"
			print item2
			print "========"
			num=item2.find(name='span',attrs={'class':'num'},recursive=False)
			meaning["num"]=num.text
			st=item2.find(name='span',attrs={'class':'st'},recursive=False)
			st2=soup_copy(st)
			print st2
			tips=st2.find(name='div',attrs={'class':'tips_main'},recursive=False)
			print "!!!"
			print tips
			meaning["type"]={}
			meaning["type"]["cn"]=tips.get_text(strip=True)
#print type(tips.text)
#		print type(tips.get_text())
#		print "!!!!!!!!!!!!!!!!!!"
			tips.extract()
			meaning["type"]["en"]=st2.get_text(strip=True)
			blue=item2.find(name='span',attrs={'class':'text_blue'},recursive=False)
			meaning["meaning_cn"]=blue.text
#item2_2=soup_copy(item2)
#		tmp=item2_2.findAll(name='span',attrs={'class':['num','st','tips_box','text_blue']})
#		[x.extract() for x in tmp]
#		meaning["meaning_en"]=item2_2.text
			mean_en=""
			print "?????????"
			for cont in item2.contents:
				print unicode(cont)
				if type(cont)==bs4.element.NavigableString:
					mean_en+=unicode(cont)
				elif type(cont)==bs4.element.Tag:
					print cont.name
					if(cont.name=="b"):
						mean_en+=unicode(cont)
			meaning["meaning_en"]=mean_en.strip()
			print "!!!!!!!!!"
#raw_input()
#print unicode(item2_2.string)
#		print "xxxxx"
#print dir(item)
			examples=item.ul.findAll(name='li',attrs={'class':None},recursive=False)
			meaning["examples"]=[]
			for example in examples:
				e_dict={}
				e_dict['en']=example.findAll(name='p')[0].get_text(strip=True)
				e_dict['cn']=example.findAll(name='p')[1].get_text(strip=True)
				meaning["examples"].append(e_dict)
			'''
			print "00000"
			print example
			print "aaaaa"
			print tmp
			print "bbbbb"
			print type(st.text)'''
#print meaning["st"]
			print_dict(meaning)
			collins_dict["meanings"].append(meaning)
	collins_pack["list"].append(collins_dict)
print "##################################"
print "##################################"
print "##################################"
print "##################################"
print "##################################"
print_dict(collins_pack)

#for x in soup.findAll("div",attrs={"class":"collins"}):
#	print "!!!"
#print item2.append
#print dir(item)

#collins=soup.find("div",attrs={"class":"collins_content"})
#return str(collins.content[0]	
