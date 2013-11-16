#! /usr/bin/env python3
# coding: utf-8
import urllib.request
#~ from bs4 import BeautifulSoup
import sys
import json

def del_tags(string):
	res = ''
	skip_flag = 0
	for char in string:
		if char == '>':
			skip_flag = 0
			continue
		if skip_flag:
			continue
		else:
			if char == '<':
				skip_flag = 1
				continue
		res += char
	return res
def add_to_file(what_add, target_file, end='\n'):
	outfile = open(target_file, 'a+')
	outfile.write( str(what_add) + end )
	outfile.close()
def get_page_content(url):
	page = urllib.request.urlopen(url)
	return page.read().decode(encoding='UTF-8')
def get_refs(page):
	res = []
	st = page.find('>Примечания</span>')
	if st != -1:
		cn = 1
		while True:
			st = page[st:].find('<p class=') + len(page[:st])
			if st != -1:
				fn = page[st:].find('</p>') + len(page[:st])
				reftext = del_tags(page[st:fn])
				if reftext:
					res.append(reftext)
					cn += 1
					st += len(reftext) + 8
				else:
					break
			else:
				break
	return res
def cut_start(book):
	start_sign = '[А] [Б] [В] [Г] [Д] [Е] [Ж] [З] [И] [Й] [К] [Л] [М] [Н] [О] [П] [Р] [С] [Т] [У] [Ф] [Х] [Ц] [Ч] [Ш] [Щ] [Э] [Ю] [Я]'
	book = book[book.find(start_sign):]
	bookst = book.find('\n')
	return book[bookst:]

page = get_page_content(sys.argv[1])
title = sys.argv[2]
print('Page is getted ({} characters), processing...'.format(len(page)))

for idx, ref in enumerate(get_refs(page)): page = page.replace('['+str(idx+1)+']', '['+ref+']')
book = del_tags(page)
book = cut_start(book)

add_to_file(book, target_file=title+'.txt', end='\n')
