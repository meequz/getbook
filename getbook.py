#! /usr/bin/env python3
# coding: utf-8
import urllib.request
import sys

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
def write_to_file(what_add, target_file, end='\n'):
	outfile = open(target_file, 'w')
	outfile.write( str(what_add) + end )
	outfile.close()
def get_page_content(url):
	page = urllib.request.urlopen(url)
	return page.read().decode(encoding='UTF-8')
def get_refs(page):
	res = []
	st = page.find('<a name="n_1"></a>')
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
	start_sign = '[Ю] [Я]'
	book = book[book.find(start_sign):]
	bookst = book.find('\n')
	return book[bookst:]
def del_empty_lines(sometext):
	work = sometext.split('\n')
	res = []
	skipflag = 0
	for idx, line in enumerate(work):
		if skipflag:
			skipflag = 0
			continue
		if line:
			res.append(line)
			continue
		try:
			if not work[idx+1]:
				res.append(line)
				skipflag = 1
				continue
		except IndexError:
			break
	return '\n'.join(res)
def strip_lines(sometext):
	work = sometext.split('\n')
	res = [line.strip() for line in work]
	return '\n'.join(res)

page = get_page_content(sys.argv[1])
title = sys.argv[2]
print('Page received ({} characters), processing...'.format(len(page)))

page = page.replace('<p class=', '\n<p class=')
for idx, ref in enumerate(get_refs(page)): page = page.replace('['+str(idx+1)+']', '['+ref+']')

book = del_tags(page)
book = cut_start(book)
book = strip_lines(book)
book = del_empty_lines(book)

write_to_file(book, target_file=title+'.txt', end='\n')
print('Done:', title+'.txt')
